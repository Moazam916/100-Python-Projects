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
    """

    import time

    sfn = boto3.client("stepfunctions")
    paginator = sfn.get_paginator("list_executions")
    results: list[Dict[str, Any]] = []

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
            results.append(
                {
                    "executionArn": arn,
                    "name": name,
                    "rule_key": rule_key,
                    "cause": cause,
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
