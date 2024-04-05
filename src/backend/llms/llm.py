import tiktoken
from enum import Enum


class Unit(Enum):
    characters = "chars"
    tokens = "tokens"


class Encoding(Enum):
    none = "not applicable"
    cl100k_base = "cl100k_base"


class Provider(Enum):
    openai = "openai"
    anthropic = "anthropic"
    google = "google"
    mistral = "mistral"
    cohere = "cohere"


class LLMModel:
    def __init__(
        self,
        name: str,
        provider: Provider,
        encoding: Encoding,
        unit: Unit,
        context: int,
        input_price: float,
        output_price: float,
    ):
        self.name = name
        self.provider = provider
        self.encoding = encoding
        self.unit = unit
        self.context = context
        self.input_price = input_price
        self.output_price = output_price

    def calculate_units(self, input_message: str, output_message: str) -> int:
        enc = tiktoken.get_encoding(self.encoding.value)
        input = len(enc.encode(input_message))
        output = len(enc.encode(output_message))
        return input, output

    def calculate_cost(self, input: int, output: int) -> float:
        print("Not implemented")
        pass


class GPT3_5_Turbo(LLMModel):
    def __init__(self):
        super().__init__(
            "GPT-3.5 Turbo",
            Provider.openai,
            Encoding.cl100k_base,
            Unit.tokens,
            16000,
            0.0005,
            0.0015,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class GPT3_5_Turbo_Finetuned(LLMModel):
    def __init__(self):
        super().__init__(
            "GPT-3.5 Turbo (fine-tuned)",
            Provider.openai,
            Encoding.cl100k_base,
            Unit.tokens,
            4000,
            0.003,
            0.006,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class GPT4_8K(LLMModel):
    def __init__(self):
        super().__init__(
            "GPT-4 8K",
            Provider.openai,
            Encoding.cl100k_base,
            Unit.tokens,
            8000,
            0.03,
            0.06,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class GPT4_32K(LLMModel):
    def __init__(self):
        super().__init__(
            "GPT-4 32K",
            Provider.openai,
            Encoding.cl100k_base,
            Unit.tokens,
            32000,
            0.06,
            0.12,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class GPT4_Turbo(LLMModel):
    def __init__(self):
        super().__init__(
            "GPT-4 Turbo",
            Provider.openai,
            Encoding.cl100k_base,
            Unit.tokens,
            128000,
            0.01,
            0.03,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class Gemini_Pro_1(LLMModel):
    def __init__(self):
        super().__init__(
            "Gemini Pro 1.0",
            Provider.google,
            Encoding.cl100k_base,
            Unit.tokens,
            32000,
            0.0005,
            0.0015,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)
    
class Gemini_Pro_1_5(LLMModel):
    def __init__(self):
        super().__init__(
            "Gemini Pro 1.5",
            Provider.google,
            Encoding.cl100k_base,
            Unit.tokens,
            1000000,
            0.007,
            0.021,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class Mistral_Small(LLMModel):
    def __init__(self):
        super().__init__(
            "Mistral Small",
            Provider.mistral,
            Encoding.cl100k_base,
            Unit.tokens,
            32000,
            0.002,
            0.006,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class Mistral_Medium(LLMModel):
    def __init__(self):
        super().__init__(
            "Mistral Medium",
            Provider.mistral,
            Encoding.cl100k_base,
            Unit.tokens,
            32000,
            0.0027,
            0.0081,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class Mistral_Large(LLMModel):
    def __init__(self):
        super().__init__(
            "Mistral Large",
            Provider.mistral,
            Encoding.cl100k_base,
            Unit.tokens,
            32000,
            0.008,
            0.024,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class Claude_Haiku(LLMModel):
    def __init__(self):
        super().__init__(
            "Claude Haiku",
            Provider.anthropic,
            Encoding.cl100k_base,
            Unit.tokens,
            200000,
            0.00025,
            0.00125,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class Claude_Sonnet(LLMModel):
    def __init__(self):
        super().__init__(
            "Claude Sonnet",
            Provider.anthropic,
            Encoding.cl100k_base,
            Unit.tokens,
            200000,
            0.003,
            0.015,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class Claude_Opus(LLMModel):
    def __init__(self):
        super().__init__(
            "Claude Opus",
            Provider.anthropic,
            Encoding.cl100k_base,
            Unit.tokens,
            200000,
            0.015,
            0.075,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class Claude_2_1(LLMModel):
    def __init__(self):
        super().__init__(
            "Claude 2.1",
            Provider.anthropic,
            Encoding.cl100k_base,
            Unit.tokens,
            200000,
            0.008,
            0.024,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class Claude_2_0(LLMModel):
    def __init__(self):
        super().__init__(
            "Claude 2.0",
            Provider.anthropic,
            Encoding.cl100k_base,
            Unit.tokens,
            100000,
            0.008,
            0.024,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class Claude_Instant(LLMModel):
    def __init__(self):
        super().__init__(
            "Claude Instant",
            Provider.anthropic,
            Encoding.cl100k_base,
            Unit.tokens,
            100000,
            0.0008,
            0.0024,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class Command_R(LLMModel):
    def __init__(self):
        super().__init__(
            "Command R",
            Provider.cohere,
            Encoding.cl100k_base,
            Unit.tokens,
            128000,
            0.0005,
            0.0015,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class Command_Light(LLMModel):
    def __init__(self):
        super().__init__(
            "Command Light",
            Provider.cohere,
            Encoding.cl100k_base,
            Unit.tokens,
            8000,
            0.0003,
            0.0006,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)


class Command_Light_Finetuned(LLMModel):
    def __init__(self):
        super().__init__(
            "Command Light (fine-tuned)",
            Provider.cohere,
            Encoding.cl100k_base,
            Unit.tokens,
            8000,
            0.0003,
            0.0006,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * (
            input / 1000
        ) + self.output_price * (output / 1000)
