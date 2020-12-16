# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import random
import requests


def main(name: str) -> str:
    number = random.randint(1111, 9999)
    response = {
        "body": f"Your verification code is {number}",
        "to": name
    }
    requests.post("https://haritest.free.beeceptor.com", json=response)
    return response
