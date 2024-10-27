import requests

def create_new_order(email, menuid, quantity, address , instruction, date):
    url = "https://fake-menu.onrender.com/create_order"

    order_details = {
        "email": email,
        "menuid": menuid,
        "quantity": quantity,
        "address": address,
        "instruction": instruction,
        "status": 'Placed',
        "date": date
        }

    try:
        response = requests.post(url, json=order_details)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as err:
        return f"HTTP error: {err}"
    except Exception as e:
        return f"Error: {str(e)}"