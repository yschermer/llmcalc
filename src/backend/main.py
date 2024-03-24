from flask import Flask, jsonify, request

from calc import calculate_cost_by_messages, calculate_cost_by_tokens, models_info

app = Flask(__name__)

@app.route("/models")
def models():
    models = models_info()
    return jsonify(models)


@app.route("/calc/messages", methods=["POST"])
def calculate_messages():
    data = request.json
    input_message = data.get("input_message")
    output_message = data.get("output_message")
    api_calls = int(data.get("api_calls"))

    costs = calculate_cost_by_messages(input_message, output_message, api_calls)
    return jsonify(costs)


@app.route("/calc/tokens", methods=["POST"])
def calculate_tokens():
    data = request.json
    input_tokens = int(data.get("input_tokens"))
    output_tokens = int(data.get("output_tokens"))
    api_calls = int(data.get("api_calls"))

    costs = calculate_cost_by_tokens(input_tokens, output_tokens, api_calls)
    return jsonify(costs)


if __name__ == "__main__":
    app.run(debug=True)
