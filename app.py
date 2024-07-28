from flask import Flask, request, jsonify
from handlers import handle_greeting_intent, handle_order_status_request, handle_order_status_update, handle_end_intent

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    query_result = req.get('queryResult', {})
    intent_name = query_result.get('intent', {}).get('displayName', '')

    print(f"Received intent: {intent_name}")

    intent_handlers = {
        'Greeting Intent': lambda: handle_greeting_intent("Maryam"),
        'OrderStatusRequest': handle_order_status_request,
        'OrderStatusUpdate': lambda: handle_order_status_update(query_result.get('parameters', {}).get('orderID')),
        'End': handle_end_intent
    }

    handler = intent_handlers.get(intent_name)
    if handler:
        response = handler()
        return jsonify(response)
    else:
        return jsonify({'fulfillmentText': 'Unknown intent.'}), 400

if __name__ == '__main__':
    app.run()
