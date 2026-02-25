"""Unit tests for the step function failure analyser lambda."""

from __future__ import annotations

import json
import time

import boto3
import pytest
from botocore.stub import Stubber

from stepFunction_execution_analyzer import main


@pytest.fixture(autouse=True)
def stub_sfn(monkeypatch):
    """Stub the Step Functions client so we don't hit AWS.

    Tests assume that ``main`` will create its own client when
    ``_list_failed_executions`` is called, so we patch ``boto3.client`` to
    return a stubber-wrapped client instead.
    """
    client = boto3.client("stepfunctions", region_name="us-east-1")
    stub = Stubber(client)
    monkeypatch.setattr(boto3, "client", lambda *args, **kw: client)
    return stub



def test_scan_failed_executions_single_page(stub_sfn):
    arn = "arn:aws:states:us-east-1:123:stateMachine:foo"
    # the paginator will list a single failed execution
    list_resp = {"executions": [{"name": "run1", "executionArn": "arn:exec:1", "startDate": "ignored"}]}
    stub_sfn.add_response("list_executions", list_resp, {"stateMachineArn": arn, "statusFilter": "FAILED"})
    # when we describe the execution we return input containing a rule key
    describe_resp = {
        "executionArn": "arn:exec:1",
        "input": json.dumps({"rule_key": "myrule"}),
        "status": "FAILED",
        "cause": "something broke",
    }
    stub_sfn.add_response("describe_execution", describe_resp, {"executionArn": "arn:exec:1"})
    # history call returns nothing
    stub_sfn.add_response(
        "get_execution_history",
        {"events": []},
        {"executionArn": "arn:exec:1", "maxResults": 1000},
    )
    stub_sfn.activate()

    result = main._scan_failed_executions(arn)
    assert result == [
        {
            "executionArn": "arn:exec:1",
            "name": "run1",
            "rule_key": "myrule",
            "cause": "something broke",
            "task_failures": [],
        }
    ]


def test_lambda_handler_missing_env():
    # if the env var isn't set we should get a 400 error
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.delenv("STATE_MACHINE_ARN", raising=False)
    ret = main.lambda_handler({}, None)
    assert ret["statusCode"] == 400
    assert "Missing STATE_MACHINE_ARN" in json.loads(ret["body"])
    monkeypatch.undo()


def test_time_filtering(stub_sfn, monkeypatch):
    """Executions older than 24h should be skipped."""
    arn = "arn:aws:states:us-east-1:123:stateMachine:foo"
    monkeypatch.setenv("STATE_MACHINE_ARN", arn)
    # fake current time
    fake_now = 1_600_000_000
    monkeypatch.setattr("time.time", lambda: fake_now)

    # create two executions: one old and one new
    old_start = fake_now - 90000  # 25h ago
    list_resp = {"executions": [
        {"name": "old", "executionArn": "arn:exec:old", "startDate": old_start},
        {"name": "new", "executionArn": "arn:exec:new", "startDate": fake_now},
    ]}
    stub_sfn.add_response("list_executions", list_resp, {"stateMachineArn": arn, "statusFilter": "FAILED"})

    # describe calls for both (handler should only return the new one)
    for arn_val in ("arn:exec:old", "arn:exec:new"):
        stub_sfn.add_response(
            "describe_execution",
            {
                "executionArn": arn_val,
                "input": json.dumps({}),
                "status": "FAILED",
                "cause": "x",
            },
            {"executionArn": arn_val},
        )
        stub_sfn.add_response(
            "get_execution_history",
            {"events": []},
            {"executionArn": arn_val, "maxResults": 1000},
        )
    stub_sfn.activate()

    ret = main.lambda_handler({}, None)
    assert ret["failed_executions"] == [
        {
            "executionArn": "arn:exec:new",
            "name": "new",
            "rule_key": None,
            "cause": "x",
            "task_failures": [],
        }
    ]


def test_lambda_handler_success(stub_sfn, monkeypatch):
    arn = "arn:aws:states:us-east-1:123:stateMachine:foo"
    # set env var so handler knows which state machine to query
    monkeypatch.setenv("STATE_MACHINE_ARN", arn)
    # fix the current time so our 24h cutoff is deterministic
    fake_now = 1_600_000_000
    monkeypatch.setattr("time.time", lambda: fake_now)

    # stub list + describe for a single failure that started recently
    list_resp = {"executions": [{"name": "runA", "executionArn": "arn:exec:A", "startDate": fake_now}]}
    stub_sfn.add_response("list_executions", list_resp, {"stateMachineArn": arn, "statusFilter": "FAILED"})
    describe_resp = {
        "executionArn": "arn:exec:A",
        "input": json.dumps({"ruleKey": "xyz"}),
        "status": "FAILED",
        "cause": "oops",
    }
    stub_sfn.add_response("describe_execution", describe_resp, {"executionArn": "arn:exec:A"})
    stub_sfn.add_response(
        "get_execution_history",
        {"events": []},
        {"executionArn": "arn:exec:A", "maxResults": 1000},
    )
    stub_sfn.activate()

    ret = main.lambda_handler({}, None)
    assert ret == {
        "failed_executions": [
            {
                "executionArn": "arn:exec:A",
                "name": "runA",
                "rule_key": "xyz",
                "cause": "oops",
                "task_failures": [],
            }
        ]
    }


def test_history_parsing(stub_sfn):
    """Ensure that errors from task failures are returned to the caller."""
    arn = "arn:aws:states:us-east-1:123:stateMachine:foo"
    list_resp = {"executions": [{"name": "runX", "executionArn": "arn:exec:X", "startDate": "ignored"}]}
    stub_sfn.add_response("list_executions", list_resp, {"stateMachineArn": arn, "statusFilter": "FAILED"})
    describe_resp = {
        "executionArn": "arn:exec:X",
        "input": json.dumps({}),
        "status": "FAILED",
        "cause": "top-level",
    }
    stub_sfn.add_response("describe_execution", describe_resp, {"executionArn": "arn:exec:X"})
    # provide a fake history with a couple of events: one failure and one
    # unrelated event to ensure filtering works
    history_resp = {
        "events": [
            {
                "type": "TaskFailed",
                "stateEnteredEventDetails": {"name": "DoStuff"},
                "taskFailedEventDetails": {"error": "GlueJobError", "cause": "Job xyz failed"},
            },
            {
                "type": "TaskSucceeded",
                "stateEnteredEventDetails": {"name": "Other"},
            },
        ]
    }
    stub_sfn.add_response(
        "get_execution_history",
        history_resp,
        {"executionArn": "arn:exec:X", "maxResults": 1000},
    )
    stub_sfn.activate()

    result = main._scan_failed_executions(arn)
    assert result == [
        {
            "executionArn": "arn:exec:X",
            "name": "runX",
            "rule_key": None,
            "cause": "top-level",
            "task_failures": [
                {"state": "DoStuff", "error": "GlueJobError", "cause": "Job xyz failed"}
            ],
        }
    ]


def test_history_parsing_lambda_and_activity(stub_sfn):
    """Different failure event types should all be captured by the parser."""
    arn = "arn:aws:states:us-east-1:123:stateMachine:foo"
    list_resp = {"executions": [{"name": "runY", "executionArn": "arn:exec:Y", "startDate": "ignored"}]}
    stub_sfn.add_response("list_executions", list_resp, {"stateMachineArn": arn, "statusFilter": "FAILED"})
    describe_resp = {
        "executionArn": "arn:exec:Y",
        "input": json.dumps({}),
        "status": "FAILED",
        "cause": "another top",
    }
    stub_sfn.add_response("describe_execution", describe_resp, {"executionArn": "arn:exec:Y"})
    # simulate a LambdaFunctionFailed and ActivityFailed event
    history_resp = {
        "events": [
            {
                "type": "LambdaFunctionFailed",
                "stateEnteredEventDetails": {"name": "CallLambda"},
                "lambdaFunctionFailedEventDetails": {"error": "LambdaError", "cause": "Exception in handler"},
            },
            {
                "type": "ActivityFailed",
                "stateEnteredEventDetails": {"name": "DoActivity"},
                "activityFailedEventDetails": {"error": "ActivityError", "cause": "something went wrong"},
            },
        ]
    }
    stub_sfn.add_response(
        "get_execution_history",
        history_resp,
        {"executionArn": "arn:exec:Y", "maxResults": 1000},
    )
    stub_sfn.activate()

    result = main._scan_failed_executions(arn)
    assert result == [
        {
            "executionArn": "arn:exec:Y",
            "name": "runY",
            "rule_key": None,
            "cause": "another top",
            "task_failures": [
                {"state": "CallLambda", "error": "LambdaError", "cause": "Exception in handler"},
                {"state": "DoActivity", "error": "ActivityError", "cause": "something went wrong"},
            ],
        }
    ]
