from llms.llm import (
    Command_Light,
    Command_Light_Finetuned,
    Command_R,
    GPT3_5_Turbo,
    GPT4_8K,
    GPT4_32K,
    GPT3_5_Turbo_Finetuned,
    GPT4_Turbo,
    Gemini_Pro_1,
    Gemini_Pro_1_5,
    Mistral_Small,
    Mistral_Medium,
    Mistral_Large,
    Claude_Haiku,
    Claude_Sonnet,
    Claude_Opus,
    Claude_2_1,
    Claude_2_0,
    Claude_Instant,
)
from llms.llm import Unit


def calculate_cost_by_messages(
    input_message: str, output_message: str, api_calls: int = 1
) -> list[dict[str, float]]:
    costs = []
    for llm in llms:
        input, output = llm.calculate_units(
            input_message, output_message
        )
        cost = llm.calculate_cost(input, output)
        total = cost * api_calls
        costs.append(
            {
                "model": llm,
                "cost": cost,
                "total": total,
                "input": input,
                "output": output,
            }
        )

    return costs


def calculate_units(
    input_message: str, output_message: str
) -> list[dict[str, float]]:
    input_tokens, output_tokens = (
        gpt_3_5_turbo.calculate_units(input_message, output_message)
    )
    input_characters = len(input_message)
    output_characters = len(output_message)

    return [
        {"unit": Unit.tokens, "input": input_tokens, "output": output_tokens},
        {"unit": Unit.characters, "input": input_characters, "output": output_characters},
    ]

def get_llm_by_name(name: str):
    for llm in llms:
        if llm.name == name:
            return llm
    return None

gpt_3_5_turbo = GPT3_5_Turbo()
gpt_3_5_turbo_finetuned = GPT3_5_Turbo_Finetuned()
gpt_4_8k = GPT4_8K()
gpt_4_32k = GPT4_32K()
gpt_4_turbo = GPT4_Turbo()
gemini_pro_1 = Gemini_Pro_1()
gemini_pro_1_5 = Gemini_Pro_1_5()
mistral_small = Mistral_Small()
mistral_medium = Mistral_Medium()
mistral_large = Mistral_Large()
claude_haiku = Claude_Haiku()
claude_sonnet = Claude_Sonnet()
claude_opus = Claude_Opus()
claude_2_1 = Claude_2_1()
claude_2_0 = Claude_2_0()
claude_instant = Claude_Instant()
command_r = Command_R()
command_light = Command_Light()
command_light_finetuned = Command_Light_Finetuned()
llms = [
    gpt_4_turbo,
    gpt_4_32k,
    gpt_4_8k,
    gpt_3_5_turbo,
    gpt_3_5_turbo_finetuned,
    gemini_pro_1,
    gemini_pro_1_5,
    claude_opus,
    claude_sonnet,
    claude_haiku,
    claude_2_1,
    claude_2_0,
    claude_instant,
    mistral_large,
    mistral_medium,
    mistral_small,
    command_r,
    command_light,
    command_light_finetuned,
]