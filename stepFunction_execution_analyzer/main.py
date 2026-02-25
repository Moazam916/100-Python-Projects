"""Lambda for scanning Step Function executions and reporting failures.

This module provides a `lambda_handler` compatible with AWS Lambda.  The
Lambda no longer requires the caller to supply a "rule key"; instead it
reads the ARN of the state machine to query from the
``STATE_MACHINE_ARN`` environment variable.  The function walks through
all failed executions and, for each one, uses ``describe_execution`` to
pull the original input payload and the failure cause.  The payload is
inspected for a ``rule_key``/``ruleKey`` field so that the response can
include whatever rule triggered the execution.

The return value is a JSON-serializable dictionary containing a list of
objects with the execution ARN, name, extracted rule key (if any), and
failure cause.  This information can be written to S3, sent via SNS, or
simply returned to the caller.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _extract_rule_key_from_input(execution_input: str) -> str | None:
    """Pull ``rule_key``/``ruleKey`` out of execution input JSON.

    The Step Function input payload is a string; we attempt to parse it as
    JSON and then look for the expected key name.  If parsing fails or the
    key isn't present we return ``None``.
    """

    try:
        data = json.loads(execution_input)
    except (ValueError, TypeError):
        return None

    return data.get("rule_key") or data.get("ruleKey")


def _scan_failed_executions(
    state_machine_arn: str, since_ts: float | None = None
) -> list[Dict[str, Any]]:
    """Return details about failed executions of a state machine.

    Parameters
    ----------
    state_machine_arn
        ARN of the state machine to search.
    since_ts
        If provided, only executions whose ``startDate`` is greater than or
        equal to this POSIX timestamp are considered.  The timestamp should
        use ``time.time()`` semantics (UTC seconds since epoch).

    The returned list contains dictionaries with these keys:

    * ``executionArn`` - ARN of the execution
    * ``name`` - execution name assigned when started
    * ``rule_key`` - value pulled from the execution input, if available
    * ``cause`` - failure reason text from ``describe_execution``
    * ``task_failures`` - list of dictionaries describing individual
      errors discovered in the execution history.  Each entry has ``state``,
      ``error`` and ``cause`` fields and helps surface the underlying
      Lambda/Glue/Activity/other component-level error that triggered the
      failure.  Only events that indicate a failure (those with a
      ``*FailedEventDetails`` payload) are returned; all successful or
      unrelated history events are ignored.
    """

    import time

    sfn = boto3.client("stepfunctions")
    paginator = sfn.get_paginator("list_executions")
    results: list[Dict[str, Any]] = []

    def _parse_history(execution_arn: str) -> list[Dict[str, str]]:
        """Pull failure details out of the execution history.

        We ask Step Functions for the history up to 1000 events and look for
        the kinds of events that indicate a task failed.  The structure of
        the returned event object varies slightly depending on the service
        that failed (``TaskFailed`` is generic, ``LambdaFunctionFailed`` is
        returned for lambda integrations, etc.) but both expose ``error`` and
        ``cause`` fields.  We also attempt to capture the name of the state
        so that callers can easily identify which component failed.

        The return value is a list of dictionaries with keys ``state``,
        ``error`` and ``cause``.  If there is any issue fetching the history
        (e.g. permissions) we log the exception and return an empty list so
        that the rest of the scanning still succeeds.
        """

        try:
            history_resp = sfn.get_execution_history(
                executionArn=execution_arn, maxResults=1000
            )
        except ClientError:  # pragma: no cover - external dependency
            logger.exception("unable to fetch execution history for %s", execution_arn)
            return []

        failures: list[Dict[str, str]] = []
        for ev in history_resp.get("events", []):
            # look for any event that indicates a failure; the exact type
            # varies (TaskFailed, LambdaFunctionFailed, ActivityFailed, etc)
            # but they all embed an ``*FailedEventDetails`` object containing
            # error/cause.  We also grab the name of the state if available so
            # callers can identify which step failed.
            details = None
            for key, val in ev.items():
                if key.endswith("FailedEventDetails"):
                    details = val
                    break

            if not details:
                continue

            state = ev.get("stateEnteredEventDetails", {}).get("name")
            failures.append(
                {
                    "state": state,
                    "error": details.get("error"),
                    "cause": details.get("cause"),
                }
            )
        return failures

    for page in paginator.paginate(
        stateMachineArn=state_machine_arn, statusFilter="FAILED"
    ):
        for exe in page.get("executions", []):
            start = exe.get("startDate")
            if since_ts is not None and start is not None:
                if start.timestamp() < since_ts:
                    continue

            arn = exe["executionArn"]
            name = exe.get("name")
            # fetch additional details to extract input/cause
            desc = sfn.describe_execution(executionArn=arn)
            rule_key = _extract_rule_key_from_input(desc.get("input", ""))
            cause = desc.get("cause")
            # also include any task-specific failures found in history
            history_failures = _parse_history(arn)
            results.append(
                {
                    "executionArn": arn,
                    "name": name,
                    "rule_key": rule_key,
                    "cause": cause,
                    "task_failures": history_failures,
                }
            )
    return results


# ---------------------------------------------------------------------------
# Lambda entry point
# ---------------------------------------------------------------------------

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """AWS Lambda handler.

    The event should provide a ``rule_key`` (or ``ruleKey``) containing the
    state machine ARN.  Example event::

        {
            "rule_key": "arn:aws:states:us-east-1:123456789012:stateMachine:MySM"
        }

    Returns a dict that can be JSON serialized with the failed executions.
    """

    # the state machine ARN must be supplied via environment variable
    state_machine = os.environ.get("STATE_MACHINE_ARN")
    if not state_machine:
        msg = "Missing STATE_MACHINE_ARN environment variable"
        logger.error(msg)
        return {"statusCode": 400, "body": json.dumps(msg)}

    logger.info("querying failed executions for %s", state_machine)

    # only look back 24 hours
    import time

    since = time.time() - 86400
    try:
        failed = _scan_failed_executions(state_machine, since_ts=since)
    except ClientError as err:  # pragma: no cover - external dependency
        logger.exception("AWS client error")
        return {"statusCode": 500, "body": json.dumps(str(err))}

    response = {"failed_executions": failed}
    logger.info("returning %d failures", len(failed))
    return response
