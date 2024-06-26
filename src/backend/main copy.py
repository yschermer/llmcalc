import ast
from flask import Flask, render_template_string, request, render_template
from llms.calc import calculate_cost_by_messages, calculate_units

app = Flask(__name__)
pinned_models = ["GPT-4 Turbo"]

@app.route("/")
def index():
    units = calculate_units("Here goes the input to the LLM", "Here goes the output of the LLM")
    costs = calculate_cost_by_messages("Here goes the input to the LLM", "Here goes the output of the LLM", 1)
    return render_template("index.html", units=units, costs=costs, pinned_models=pinned_models)


@app.route("/calc/messages", methods=["POST"])
def calculate_messages():
    input_message = request.form.get("input_message")
    output_message = request.form.get("output_message")
    api_calls = int(request.form.get("api_calls"))

    costs = calculate_cost_by_messages(input_message, output_message, api_calls)

    return render_template_string(
        """
        {% for cost in costs %}
            {% if cost.model.name.startswith("GPT") %}
                {% set bgColor = "bg-emerald-800" %}
            {% elif cost.model.name.startswith("Gemini") %}
                {% set bgColor = "bg-teal-800" %}
            {% elif cost.model.name.startswith("Claude") %}
                {% set bgColor = "bg-cyan-800" %}
            {% elif cost.model.name.startswith("Mistral") %}
                {% set bgColor = "bg-sky-800" %}
            {% elif cost.model.name.startswith("Command") %}
                {% set bgColor = "bg-indigo-800" %}
            {% else %}
            {% endif %}
            <tr class="{{ bgColor }}">
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
                    <button class="text-indigo-500 hover:text-indigo-600" hx-post="/pin-model"
                        hx-target="#pinned-models" hx-swap="beforeend"
                        hx-vals='{"model": "{{ cost.model.name }}"}'>
                        Pin
                    </button>
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

    costs = calculate_cost_by_messages("Here goes the input to the LLM", "Here goes the output of the LLM", 1)
    pinned_costs = [cost for cost in costs if cost.model.name in pinned_models]

    return render_template_string(
        """
        {% for cost in pinned_costs %}
            {% if cost.model.name.startswith("GPT") %}
                {% set bgColor = "bg-green-800" %}
            {% elif cost.model.name.startswith("Gemini") %}
                {% set bgColor = "bg-teal-800" %}
            {% elif cost.model.name.startswith("Claude") %}
                {% set bgColor = "bg-blue-800" %}
            {% elif cost.model.name.startswith("Mistral") %}
                {% set bgColor = "bg-indigo-800" %}
            {% elif cost.model.name.startswith("Command") %}
                {% set bgColor = "bg-purple-800" %}
            {% else %}
            {% endif %}
            <tr class="{{ bgColor }}">
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
                        <button class="text-red-500 hover:text-red-600">Unpin</button>
                    </form>
                </td>
            </tr>
        {% endfor %}
        """,
        pinned_costs=pinned_costs,
    )


if __name__ == "__main__":
    app.run(debug=True)
