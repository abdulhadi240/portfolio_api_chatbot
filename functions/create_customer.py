import requests

def create_new_customers(firstname, lastname, email, phonenumber, date):
    url = "https://fake-menu.onrender.com/create_costumers"

    customer_data = {
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "phonenumber": phonenumber,
        "date": date
    }

    try:
        response = requests.post(url, json=customer_data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as err:
        return f"HTTP error: {err}"
    except Exception as e:
        return f"Error: {str(e)}"