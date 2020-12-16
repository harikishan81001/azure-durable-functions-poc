# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json
from datetime import timedelta

import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    ph = context.get_input()
    challengeCode = yield context.call_activity("SendSmsChallenge", ph)
    due_time = context.current_utc_datetime + timedelta(seconds=30)
    durable_timeout_task = context.create_timer(due_time)
    authorized = False
    challenge_response_task = context.wait_for_external_event("SmsChallengeResponse")
    winning_task = yield context.task_any([challenge_response_task, durable_timeout_task])
    for i in range(3):
        if challenge_response_task == winning_task:
            if challenge_response_task.result == challengeCode:
                authorized = True
                break
            else:
                break

    if not durable_timeout_task.is_completed:
        durable_timeout_task.cancel()
    return authorized

main = df.Orchestrator.create(orchestrator_function)