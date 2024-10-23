import requests

def get_order_details():
    url = "https://fake-menu.onrender.com/get_orders"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []
    