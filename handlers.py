import requests
from datetime import datetime

SHIPMENT_API_URL = "https://orderstatusapi-dot-organization-project-311520.uc.r.appspot.com/api/getOrderStatus"

def format_date(iso_date_str):
    try:
        dt = datetime.fromisoformat(iso_date_str.replace("Z", "+00:00"))
        return dt.strftime("%A, %d %b %Y")
    except ValueError:
        return "Unknown date"

def handle_greeting_intent(name):
    return {'fulfillmentText': f"Hi, this is {name}'s bot. How can I help you?"}

def handle_order_status_request():
    return {'fulfillmentText': "Can I get your order ID?"}

def handle_order_status_update(order_id):
    if not order_id:
        return {'fulfillmentText': 'Please provide your order ID so I can check the status for you.'}

    payload = {'orderId': order_id}
    
    try:
        response = requests.post(SHIPMENT_API_URL, json=payload)
        if response.status_code == 200:
            shipment_data = response.json()
            shipment_date_iso = shipment_data.get("shipmentDate")
            shipment_date = format_date(shipment_date_iso)
            return {'fulfillmentText': f'Your order {order_id} will be shipped on {shipment_date}.'}
        else:
            return {'fulfillmentText': 'An error occurred while retrieving the order status.'}, 500

    except requests.RequestException as e:
        return {'fulfillmentText': f'An error occurred: {str(e)}'}, 500

def handle_end_intent():
    return {'fulfillmentText': 'Welcome!'}
