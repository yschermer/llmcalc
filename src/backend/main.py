from decimal import Decimal
from flask import Flask, request, render_template
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
    PricingUnit,
)
from llms.llm import Unit

app = Flask(__name__)
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


def format_float(value):
    new_value = f"{value:.6f}".rstrip("0").rstrip(".").lstrip("0") or "0"
    if "." not in new_value:
        new_value += ".00"
    elif new_value[-2] == ".":
        new_value += "0"

    if new_value.startswith("."):
        new_value = "0" + new_value
    
    return new_value


def calculate_cost_by_messages(
    input_message: str,
    output_message: str,
    api_calls: int = 1,
    pricing_unit: PricingUnit = PricingUnit.thousand,
    pinned_models: list[str] = [],
) -> list[dict[str, float]]:
    costs = []
    for llm in llms:
        input, output = llm.calculate_tokens(input_message, output_message)
        cost = llm.calculate_cost(input, output)
        total = cost * api_calls
        costs.append(
            {
                "model": llm,
                "input_price": format_float(llm.input_price * pricing_unit.value),
                "output_price": format_float(llm.output_price * pricing_unit.value),
                "cost": format_float(cost),
                "total": format_float(total),
                "input": input,
                "output": output,
            }
        )

    costs.sort(
        key=lambda x: (
            pinned_models.index(x["model"].name)
            if x["model"].name in pinned_models
            else len(pinned_models)
        )
    )
    return costs


def calculate_tokens_and_characters(
    input_message: str, output_message: str
) -> list[dict[str, float]]:
    input_tokens, output_tokens = gpt_3_5_turbo.calculate_tokens(
        input_message, output_message
    )

    return [
        {"unit": Unit.tokens, "input": input_tokens, "output": output_tokens},
        {
            "unit": Unit.characters,
            "input": len(input_message),
            "output": len(output_message),
        },
    ]


@app.route("/")
def index():
    input_message = ""
    output_message = ""
    api_calls = 1
    pricing_unit = PricingUnit["million"]
    units = calculate_tokens_and_characters(input_message, output_message)
    pinned_models = ["GPT-4 Turbo", "Claude 3 Opus", "Gemini Pro 1.5"]
    costs = calculate_cost_by_messages(
        input_message, output_message, api_calls, pricing_unit, pinned_models
    )

    return render_template(
        "index.html",
        input_message=input_message,
        output_message=output_message,
        api_calls=api_calls,
        pricing_unit=pricing_unit,
        units=units,
        costs=costs,
        pinned_models=pinned_models,
    )


@app.route("/update", methods=["POST"])
def update_page():
    input_message = request.form.get("input_message")
    output_message = request.form.get("output_message")
    try:
        api_calls = int(request.form.get("api_calls"))
    except ValueError:
        api_calls = int(request.form.get("api_calls")[:-1])
    pricing_unit = PricingUnit[request.form.get("pricing_unit")]

    pinned_model = request.form.get("pinned_model")
    pinned_models = request.form.get("pinned_models").split(",")
    if pinned_model:
        if pinned_model not in pinned_models:
            pinned_models.append(pinned_model)
        else:
            pinned_models.remove(pinned_model)

    units = calculate_tokens_and_characters(input_message, output_message)
    costs = calculate_cost_by_messages(
        input_message, output_message, api_calls, pricing_unit, pinned_models
    )

    return render_template(
        "index.html",
        input_message=input_message,
        output_message=output_message,
        api_calls=api_calls,
        pricing_unit=pricing_unit,
        units=units,
        costs=costs,
        pinned_models=pinned_models,
    )


if __name__ == "__main__":
    app.run(debug=True)
