import requests

BASE_URL = 'https://message-board.net'

# Create new user
body = {'username': 'JacobTest', 'password': 'Test'}
response = requests.post(BASE_URL + '/messaging/user', json=body)
print(response.status_code)

# Create new message
headers = {'Username': 'JacobTest', 'Password': 'Test'}
body = {'message': 'Hi everyone!'}
response = requests.post(BASE_URL + '/messaging/message/create', json=body, headers=headers)
print(response.status_code)
