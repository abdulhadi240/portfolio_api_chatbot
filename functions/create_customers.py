import requests

def create_new_customers(firstname, lastname, email, phonenumber, date):
    url = "https://fake-menu.onrender.com/create_customers"

    # Create the JSON payload
    customer_data = {
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "phonenumber": phonenumber,
        "date": date
    }

    # Make the POST request with the JSON payload
    response = requests.post(url, json=customer_data)
    
    if response.status_code == 200:
        return response.json()  # Return the response data if successful
    else:
        return(f"Error: {response.status_code}, Message: {response.text}")  # Print error message
        