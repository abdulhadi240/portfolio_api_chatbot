import requests

def create_new_complain(firstname, email, date , complain):
    url = "https://fake-menu.onrender.com/create_costumers"

    customer_data = {
        "firstname": firstname,
        "email": email,
        "date": date,
        "complain": complain
        }

    try:
        response = requests.post(url, json=customer_data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as err:
        return f"HTTP error: {err}"
    except Exception as e:
        return f"Error: {str(e)}"