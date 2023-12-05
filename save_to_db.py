import requests

def send_request(foods, menu_date):
    # Define the URL of your Node.js API
    # Replace with the actual URL of your server
    url = 'http://localhost:3000/save-food'

    # Define the data you want to send (as a Python dictionary)
    data = {
        "foods": foods,
        "menu_date": menu_date
    }

    # Send a POST request with the data
    response = requests.post(url, json=data)

    # Check the response from the server
    if response.status_code == 200:
        print('POST request successful')
        print('Response from server:', response.json())
    else:
        print('POST request failed with status code:', response.status_code)
        print('Response from server:', response.text)
