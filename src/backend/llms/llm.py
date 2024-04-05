import tiktoken
from enum import Enum


class PricingUnit(Enum):
    thousand = 1000
    million = 1000000

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

    def calculate_tokens(self, input_message: str, output_message: str) -> int:
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
            0.0000005,
            0.0000015,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class GPT3_5_Turbo_Finetuned(LLMModel):
    def __init__(self):
        super().__init__(
            "GPT-3.5 Turbo (fine-tuned)",
            Provider.openai,
            Encoding.cl100k_base,
            Unit.tokens,
            4000,
            0.0000030,
            0.0000060,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class GPT4_8K(LLMModel):
    def __init__(self):
        super().__init__(
            "GPT-4 8K",
            Provider.openai,
            Encoding.cl100k_base,
            Unit.tokens,
            8000,
            0.0000300,
            0.0000600,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class GPT4_32K(LLMModel):
    def __init__(self):
        super().__init__(
            "GPT-4 32K",
            Provider.openai,
            Encoding.cl100k_base,
            Unit.tokens,
            32000,
            0.0000600,
            0.0001200,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class GPT4_Turbo(LLMModel):
    def __init__(self):
        super().__init__(
            "GPT-4 Turbo",
            Provider.openai,
            Encoding.cl100k_base,
            Unit.tokens,
            128000,
            0.0000100,
            0.0000300,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class Gemini_Pro_1(LLMModel):
    def __init__(self):
        super().__init__(
            "Gemini Pro 1.0",
            Provider.google,
            Encoding.cl100k_base,
            Unit.tokens,
            32000,
            0.00000050,
            0.00000150,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output
    

class Gemini_Pro_1_5(LLMModel):
    def __init__(self):
        super().__init__(
            "Gemini Pro 1.5",
            Provider.google,
            Encoding.cl100k_base,
            Unit.tokens,
            1000000,
            0.00000700,
            0.00002100,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class Mistral_Small(LLMModel):
    def __init__(self):
        super().__init__(
            "Mistral Small",
            Provider.mistral,
            Encoding.cl100k_base,
            Unit.tokens,
            32000,
            0.0000020,
            0.0000060,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class Mistral_Medium(LLMModel):
    def __init__(self):
        super().__init__(
            "Mistral Medium",
            Provider.mistral,
            Encoding.cl100k_base,
            Unit.tokens,
            32000,
            0.0000027,
            0.0000081,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class Mistral_Large(LLMModel):
    def __init__(self):
        super().__init__(
            "Mistral Large",
            Provider.mistral,
            Encoding.cl100k_base,
            Unit.tokens,
            32000,
            0.0000080,
            0.0000240,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class Claude_Haiku(LLMModel):
    def __init__(self):
        super().__init__(
            "Claude 3 Haiku",
            Provider.anthropic,
            Encoding.cl100k_base,
            Unit.tokens,
            200000,
            0.00000025,
            0.00000125,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class Claude_Sonnet(LLMModel):
    def __init__(self):
        super().__init__(
            "Claude 3 Sonnet",
            Provider.anthropic,
            Encoding.cl100k_base,
            Unit.tokens,
            200000,
            0.0000030,
            0.0000150,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class Claude_Opus(LLMModel):
    def __init__(self):
        super().__init__(
            "Claude 3 Opus",
            Provider.anthropic,
            Encoding.cl100k_base,
            Unit.tokens,
            200000,
            0.0000150,
            0.0000750,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class Claude_2_1(LLMModel):
    def __init__(self):
        super().__init__(
            "Claude 2.1",
            Provider.anthropic,
            Encoding.cl100k_base,
            Unit.tokens,
            200000,
            0.0000080,
            0.0000240,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class Claude_2_0(LLMModel):
    def __init__(self):
        super().__init__(
            "Claude 2.0",
            Provider.anthropic,
            Encoding.cl100k_base,
            Unit.tokens,
            100000,
            0.0000080,
            0.0000240,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class Claude_Instant(LLMModel):
    def __init__(self):
        super().__init__(
            "Claude Instant",
            Provider.anthropic,
            Encoding.cl100k_base,
            Unit.tokens,
            100000,
            0.0000008,
            0.0000024,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class Command_R(LLMModel):
    def __init__(self):
        super().__init__(
            "Command R",
            Provider.cohere,
            Encoding.cl100k_base,
            Unit.tokens,
            128000,
            0.0000005,
            0.0000015,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class Command_Light(LLMModel):
    def __init__(self):
        super().__init__(
            "Command Light",
            Provider.cohere,
            Encoding.cl100k_base,
            Unit.tokens,
            8000,
            0.0000003,
            0.0000006,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output


class Command_Light_Finetuned(LLMModel):
    def __init__(self):
        super().__init__(
            "Command Light (fine-tuned)",
            Provider.cohere,
            Encoding.cl100k_base,
            Unit.tokens,
            8000,
            0.0000003,
            0.0000006,
        )

    def calculate_cost(self, input: float, output: float) -> float:
        return self.input_price * input + self.output_price * output
