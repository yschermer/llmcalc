import ast
from flask import Flask, render_template_string, request, render_template, session
from llms.calc import calculate_cost_by_messages, calculate_units

app = Flask(__name__)
app.secret_key = "BAD_SECRET_KEY"


@app.route("/")
def index():
    units = calculate_units(
        "Here goes the input to the LLM", "Here goes the output of the LLM"
    )
    costs = calculate_cost_by_messages(
        "Here goes the input to the LLM", "Here goes the output of the LLM", 1
    )
    pinned_costs = [
        cost for cost in costs if cost["model"].name in session.get("pinned_models", [])
    ]
    return render_template(
        "index.html", units=units, costs=costs, pinned_costs=pinned_costs
    )


@app.route("/calc/messages", methods=["POST"])
def calculate_messages():
    input_message = request.form.get("input_message")
    output_message = request.form.get("output_message")
    api_calls = int(request.form.get("api_calls"))

    costs = calculate_cost_by_messages(input_message, output_message, api_calls)

    return render_template_string(
        """
        {% for cost in costs %}
            <tr class="{{ bgColor }} hover:bg-gray-800">
                <td class="px-6 py-4 whitespace-nowrap"> <img
                        src="../static/images/{{ cost.model.provider.value }}.png"
                        alt="{{ cost.model.provider.value }} logo"
                        class="h-6 w-6 rounded-full bg-gray-300 p-1"> </td>
                <td class="px-6 py-4 whitespace-nowrap text-gray-300">{{ cost.model.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-gray-400">{{
                    "$%.5f"|format(cost.model.input_price) }} <span class="text-gray-500">/ 1k {{
                        cost.model.unit.value }}</span></td>
                <td class="px-6 py-4 whitespace-nowrap text-gray-400">{{
                    "$%.5f"|format(cost.model.output_price) }} <span class="text-gray-500">/ 1k {{
                        cost.model.unit.value }}</span></td>
                <td class="px-6 py-4 whitespace-nowrap text-gray-400">{{ "$%.5f"|format(cost.cost) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-gray-300">{{ "$%.5f"|format(cost.total) }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <form hx-post="/pin-model" hx-target="#pinned-models">
                        <input type="hidden" name="model" value="{{ cost.model.name }}">
                        <button class="text-indigo-500 hover:text-indigo-600 inline-block align-middle">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>                                 
                        </button>
                    </form>
                </td>
            </tr>
        {% endfor %}
    """,
        costs=costs,
        api_calls=api_calls,
    )


@app.route("/calc/tokens", methods=["POST"])
def calculate_tokens():
    input = request.form.get("input_message")
    output = request.form.get("output_message")
    api_calls = int(request.form.get("api_calls"))

    units = calculate_units(input, output)

    return render_template_string(
        """
        <div id="calc-unit-results-input" hx-swap-oob="true">
            <p><strong class="has-text-grey-dark">{{ units[0].input }}</strong> <span class="has-text-grey">{{ units[0].unit.value }}</span></p>
            <p><strong class="has-text-grey-dark">{{ units[1].input }}</strong> <span class="has-text-grey">{{ units[1].unit.value }}</span></p>
        </div>
        <div id="calc-unit-results-output" hx-swap-oob="true">
            <p><strong class="has-text-grey-dark">{{ units[0].output }}</strong> <span class="has-text-grey">{{ units[0].unit.value }}</span></p>
            <p><strong class="has-text-grey-dark">{{ units[1].output }}</strong> <span class="has-text-grey">{{ units[1].unit.value }}</span></p>
        </div>
    """,
        units=units,
        api_calls=api_calls,
    )


@app.route("/pin-model", methods=["POST"])
def pin_model():
    model = request.form.get("model")
    pinned_models = session.get("pinned_models", [])

    if model not in pinned_models:
        pinned_models.append(model)
        session["pinned_models"] = pinned_models

    return ""


@app.route("/unpin-model", methods=["POST"])
def unpin_model():
    model = request.form.get("model")
    pinned_models = session.get("pinned_models", [])

    if model in pinned_models:
        pinned_models.remove(model)
        session["pinned_models"] = pinned_models

    return ""


@app.route("/update-pinned-models", methods=["POST"])
def update_pinned_models():
    input_message = request.form.get("input_message")
    output_message = request.form.get("output_message")
    api_calls = int(request.form.get("api_calls"))
    pinned_models = session.get("pinned_models", [])
    costs = calculate_cost_by_messages(input_message, output_message, api_calls)
    pinned_costs = [cost for cost in costs if cost["model"].name in pinned_models]
    return render_template_string(
        """
        {% for cost in pinned_costs %}
        <tr class="{{ bgColor }} hover:bg-gray-800">
            <td class="px-6 py-4 whitespace-nowrap">
                <img src="../static/images/{{ cost.model.provider.value }}.png" alt="{{ cost.model.provider.value }} logo" class="h-8 w-8 rounded-full bg-gray-300 p-1">
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-gray-300">{{ cost.model.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-gray-400">
                {{ "$%.5f"|format(cost.model.input_price) }} <span class="text-gray-500">/ 1k {{ cost.model.unit.value }}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-gray-400">
                {{ "$%.5f"|format(cost.model.output_price) }} <span class="text-gray-500">/ 1k {{ cost.model.unit.value }}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-gray-400">{{ "$%.5f"|format(cost.cost) }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-gray-300">{{ "$%.5f"|format(cost.total) }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <form hx-post="/unpin-model" hx-target="#pinned-models">
                    <input type="hidden" name="model" value="{{ cost.model.name }}">
                    <button class="text-red-500 hover:text-red-600 inline-block align-middle">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                    </button>
                </form>
            </td>
        </tr>
        {% endfor %}
        """,
        pinned_costs=pinned_costs,
    )


if __name__ == "__main__":
    app.run(debug=True)
