import tiktoken
from enum import Enum


class Encoding(Enum):
    cl100k_base = "cl100k_base"


class LLMModel:
    def __init__(
        self,
        name: str,
        encoding: Encoding,
        context: int,
        input_token_price: float,
        output_token_price: float,
    ):
        self.name = name
        self.encoding = encoding
        self.context = context
        self.input_token_price = input_token_price
        self.output_token_price = output_token_price

    def calculate_tokens(self, input_message: str, output_message: str) -> int:
        print("Not implemented")
        pass

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        print("Not implemented")
        pass


class GPT3_5_Turbo(LLMModel):
    def __init__(self):
        super().__init__("gpt-3.5-turbo", Encoding.cl100k_base, 16000, 0.0005, 0.0015)

    def calculate_tokens(self, input_message: str, output_message: str) -> int:
        enc = tiktoken.get_encoding(self.encoding.value)
        input_tokens = len(enc.encode(input_message))
        output_tokens = len(enc.encode(output_message))
        return input_tokens, output_tokens

    def calculate_cost(self, input_tokens: float, output_tokens: float) -> float:
        return self.input_token_price * (
            input_tokens / 1000
        ) + self.output_token_price * (output_tokens / 1000)


class GPT4(LLMModel):
    def __init__(self):
        super().__init__("gpt-4", Encoding.cl100k_base, 8000, 0.03, 0.06)

    def calculate_tokens(self, input_message: str, output_message: str) -> int:
        enc = tiktoken.get_encoding(self.encoding.value)
        input_tokens = len(enc.encode(input_message))
        output_tokens = len(enc.encode(output_message))
        return input_tokens, output_tokens

    def calculate_cost(self, input_tokens: float, output_tokens: float) -> float:
        return self.input_token_price * (
            input_tokens / 1000
        ) + self.output_token_price * (output_tokens / 1000)


def models_info():
    return [
        {"name": gpt_3_5_turbo.name, "input_token_price": gpt_3_5_turbo.input_token_price, "output_token_price": gpt_3_5_turbo.output_token_price},
        {"name": gpt_4.name, "input_token_price": gpt_4.input_token_price, "output_token_price": gpt_4.output_token_price},
    ]


def calculate_cost_by_messages(
    input_message: str, output_message: str, api_calls: int = 1
) -> list[dict[str, float]]:
    input_tokens, output_tokens = gpt_3_5_turbo.calculate_tokens(
        input_message, output_message
    )
    gpt_3_5_turbo_cost = (
        gpt_3_5_turbo.calculate_cost(input_tokens, output_tokens) * api_calls
    )

    input_tokens, output_tokens = gpt_4.calculate_tokens(input_message, output_message)
    gpt_4_cost = gpt_4.calculate_cost(input_tokens, output_tokens) * api_calls

    return [
        {"model_name": gpt_3_5_turbo.name, "cost": gpt_3_5_turbo_cost, "input_tokens": input_tokens, "output_tokens": output_tokens},
        {"model_name": gpt_4.name, "cost": gpt_4_cost, "input_tokens": input_tokens, "output_tokens": output_tokens},
    ]


def calculate_cost_by_tokens(
    input_tokens: int, output_tokens: int, api_calls: int = 1
) -> list[dict[str, float]]:
    gpt_3_5_turbo_cost = (
        gpt_3_5_turbo.calculate_cost(input_tokens, output_tokens) * api_calls
    )

    gpt_4_cost = gpt_4.calculate_cost(input_tokens, output_tokens) * api_calls
    
    return [
        {"model_name": gpt_3_5_turbo.name, "cost": gpt_3_5_turbo_cost},
        {"model_name": gpt_4.name, "cost": gpt_4_cost},
    ]


gpt_3_5_turbo = GPT3_5_Turbo()
gpt_4 = GPT4()
