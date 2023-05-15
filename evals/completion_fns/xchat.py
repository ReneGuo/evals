import time
import uuid

import requests

from evals.api import CompletionFn, CompletionResult
from evals.prompt.base import CompletionPrompt
from evals.record import record_sampling


class XChatCompletionResult(CompletionResult):
    def __init__(self, response) -> None:
        self.response = response

    def get_completions(self) -> list[str]:
        return [self.response.strip()]


class XChatCompletionFn(CompletionFn):
    def __init__(self, **kwargs):
        self.model_addr = kwargs['model_addr']

    def chat(self, query):
        resp = requests.post(
            self.model_addr,
            json={
                "data": [
                    query,
                    None,
                    "auto",
                    "",
                    "问题",
                    "回答",
                    "",
                    "250",
                    1,
                    50,
                    0.92,
                    0,
                    1,
                    1.2,
                ]
            },
        ).json()
        res = resp["data"][0][-1][-1]
        return res

    def __call__(self, prompt, **kwargs) -> XChatCompletionResult:
        prompt = CompletionPrompt(prompt).to_formatted_prompt()
        response = self.chat(prompt)
        record_sampling(prompt=prompt, sampled=response)
        return XChatCompletionResult(response)
