import requests

BASE_URL = 'https://message-board.net'

response = requests.get(BASE_URL + '/messaging/message')
messages = response.json()['messages']
for message in messages:
    print(f'({message['id']}) {message['username']}: {message['message']}')
