import requests

def get_menu_items():
    url = "https://fake-menu.onrender.com/menu"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []
    