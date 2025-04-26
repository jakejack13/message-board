import requests

BASE_URL = 'https://message-board.net'

# Create new user
body = {'username': 'Jacob', 'password': 'Test'}
response = requests.post(BASE_URL + '/messaging/user', json=body)
print(response.status_code)

# Create new message
headers = {'Username': 'Jacob', 'Password': 'Test'}
body = {'message': 'I made a message!'}
response = requests.post(BASE_URL + '/messaging/message/create', json=body, headers=headers)
print(response.status_code)
