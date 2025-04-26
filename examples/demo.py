import requests

BASE_URL = 'https://message-board.net'

response = requests.get(BASE_URL +'/messaging/message')
print(response.status_code)
for message in response.json()['messages']:
    print(f'{message['id']} {message['username']}: {message['message']}')


body = {'username': 'Jacob', 'password': 'testing123'}
response = requests.post(BASE_URL + '/messaging/user', json=body)
print(response.status_code)

headers = {'Username': 'Jacob', 'Password': 'testing123'}
body = {'message': '@Jacob everyone its me the demo works!'}
response = requests.post(BASE_URL + '/messaging/message/create', json=body, headers=headers)
print(response.status_code)

response = requests.get(BASE_URL +'/messaging/message/tagged', headers=headers)
print(response.status_code)
for message in response.json()['messages']:
    print(f'{message['id']} {message['username']}: {message['message']}')
