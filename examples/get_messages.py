import requests

BASE_URL = 'https://message-board.net'

query_params = {'limit': 10000}
response = requests.get(BASE_URL + '/messaging/message', params=query_params)
messages = response.json()['messages']
for message in messages:
    print(f'({message['id']}) {message['username']}: {message['message']}')
