# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json

import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    data = context.get_input()
    result1 = yield context.call_activity('IsValidStatus', json.dumps(data))
    result2 = yield context.call_activity('IsValidPlacementDt', "11/12/2020 05:10:00")
    result3 = yield context.call_activity('AssignVehicle', "HR26DG1162")
    result4 = yield context.call_activity('OrderStatusUpdate', "Placed")
    return [result1, result2, result3, result4]

main = df.Orchestrator.create(orchestrator_function)