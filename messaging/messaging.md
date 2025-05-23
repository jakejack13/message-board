# Messaging

The message board API. This API allows users to post new messages to
the message board and get all messages from the message board.

## Authorization

All requests to the API, besides the user creation endpoint and the get
all messages endpoint, requires the user to supply their username and password in the `Username`  and
`Password` headers:

```json
{
    "USERNAME": <your username>,
    "PASSWORD": <your password>
}
```

If a request fails authentication, a `401 Unauthorized` error is thrown.

## Endpoints

### Create a new user

`POST /messaging/user`

This endpoint creates a user with the given username and password and
returns the id of the user, to be used in the headers of subsequent
requests to this API. Each user's name must be unique. Usernames must be
unique. If a user supplies a username that has already been taken, a
`409 Conflict` response will be returned if the supplied password is incorrect. This means that this operation is idempotent if the correct
password is supplied for a username that already exists.

#### Request

```json
{
    "username": string,
    "password": string
}
```

#### Response

- `201 Created`: Success
- `400 Bad Request`: Username or password not supplied
- `409 Conflict`: Username has already been taken

### Get all messages

`GET /messaging/message?limit={limit:int}&since={since:int}`

This endpoint returns all of the messages on the message board. A message
consists of the username of the user that posted the message along with
the message itself and its unique id. The messages will be sent in the
order that they were created, with the most recent being the last in
the list. If the `limit` query param is supplied, only the last `limit`
number of messages are returned. If `limit` is not supplied, a default
of 100 messages is used. If the `since` query param is supplied, only
messages with a message id greater than `since` will be returned. This
is useful for if you would only like to request messages you have not
already seen.

#### Response

```json
{
    "messages": [
        {
            "id": int,
            "username": string,
            "message": string
        },
        {
            "id": int,
            "username": string,
            "message": string
        }
    ]
}
```

- `200 Ok`: Success

### Get my messages

`GET /messaging/message/me`

This endpoint returns all of the messages sent by you on the message
board. A message consists of the username of the user that posted the
message along with the message itself and its unique id. The messages
will be sent in the order that they were created, with the most recent
being the last in the list.

#### Response

```json
{
    "messages": [
        {
            "id": int,
            "username": string,
            "message": string
        },
        {
            "id": int,
            "username": string,
            "message": string
        }
    ]
}
```

### Get messages I am tagged in

`GET /messaging/message/tagged`

This endpoint returns all of the messages that has your username tagged
in it. A tag consists of the `@` symbol followed by your username, ex.
`@Jacob`. A message consists of the username of the user that posted the
message along with the message itself and its unique id. The messages will
be sent in the order that they were created, with the most recent being the
last in the list.

#### Response

```json
{
    "messages": [
        {
            "id": int,
            "username": string,
            "message": string
        },
        {
            "id": int,
            "username": string,
            "message": string
        }
    ]
}
```

- `200 Ok`: Success
- `401 Unauthorized`: Authentication failed

### Create a new message

`POST /messaging/message/create`

Creates a new message from the logged in user on the message board.

#### Request

```json
{
    "message": string
}
```

#### Response

- `201 Created`: Success
- `400 Bad Request`: Message is not supplied
- `401 Unauthorized`: Authentication failed
