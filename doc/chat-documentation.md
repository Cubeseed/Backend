# Chat Documentation

## Table of Contents
[**WebSocket Connection**](#websocket-connection)  

[Connection Establishment and Chat Endpoint](#connection-establishment-and-chat-endpoint)  
  - [Consumer Emitted Chat Message Event](#1-consumer-emitted-chat-message-event)  
  - [Consumer Emitted User Join Event](#2-consumer-emitted-user-join-event)  
  - [Consumer Emitted User Leave Event](#3-consumer-emitted-user-leave-event)  
  - [Consumer Emitted Online Users List Event](#4-consumer-emitted-online-users-list-event)  
  - [Client Emitted Messages Read Event](#5-client-emitted-messages-read-event)
  - [Client Emitted Send Message Event](#6-client-emitted-send-message-event)

[Single Conversation Based Notification Endpoint](#single-conversation-based-notification-endpoint)  
  - [Consumer Emitted Single Conversation Unread Count Event](#1-consumer-emitted-single-conversation-unread-count-event)
  - [Consumer Emitted Single Conversation New Message Notification Event](#2-consumer-emitted-single-conversation-new-message-notification-event)

[All conversations based notification endpoint](all-conversations-based-notification-endpoint)
  - [Consumer Emitted All Conversations Unread Count Event](#1-consumer-emitted-all-conversations-unread-count-event)  
  - [Consumer Emitted All Conversations New Message Notification Event](#2-consumer-emitted-all-conversations-new-message-notification-event)

[**API Endpoints Related to Chat**](#api-endpoints-related-to-chat)

- [Upload Multimedia Endpoint](#1-upload-multimedia-endpoint)
- [Check URL Validity Endpoint](#2-check-url-validity-endpoint)
- [Refresh URL Endpoint](#3-refresh-url-endpoint)
- [Get all Conversations of a User](#4get-all-conversations-of-a-user)
- [Get all Conversations within a Room](#5get-all-conversations-within-a-room)


## WebSocket Connection

#### **Connection Establishment and Chat Endpoint:**

- ws://127.0.0.1:8000/ws/${room}/

Client initiates a WebSocket connection to a specific chat room.
The variable `room` is the username of the person to chat with.

[Back to Table of Contents](#table-of-contents)

#### 1. **Consumer Emitted Chat Message Event**

- **Event Name:** `chat_message`
- **Description:** Sent when a new message is received.
- **Payload:**
  ```json
  {
    "type": "chat_message",
    "message": "Hello, world!",
    "multimedia_url": "multimedia url link",
    "date_added": "2023-11-10T19:10:30.866848Z",
    "from_user": {"username": "username"},
    "room": "room",
  }

[Back to Table of Contents](#table-of-contents)

#### 2. **Consumer Emitted User Join Event**
- **Event Name**: `user_join`
- **Description**: Sent when a user joins a chat room
- **Payload**
```json
{
    "type": "user_join",
    "user": "username",
}
```

[Back to Table of Contents](#table-of-contents)

#### 3. **Consumer Emitted User Leave Event**
- **Event Name**: `user_leave`
- **Description**: Sent when a user leaves a chat room
- **Payload**
```json
{
    "type": "user_leave",
    "user": "username",
}
```

[Back to Table of Contents](#table-of-contents)

#### 4. **Consumer Emitted Online Users List Event**
- **Event Name**: `online_user_list`
- **Description**: Sends a list of online users in a room
- **Payload**
```json
{
    "type": "online_user_list",
    "users": ["username1", "username2"]
}
```

[Back to Table of Contents](#table-of-contents)

#### 5. **Client Emitted Messages Read Event**
- **Event Name**: `read_messages`
- **Description**: Sent by the client whenever a user reads a message
- **Payload**
```json
{
    "type": "read_messages",
}
```

[Back to Table of Contents](#table-of-contents)

#### 6. **Client Emitted Send Message Event**
- **Event Name**: `chat_message`
- **Description**: Sent by the client whenever a user sends a message
- **Payload**
```json
{
    "type": "chat_message",
    "message": "text message to be sent",
    "multimedia_url": "multimediaurl or empty string",
    "file_identifier": "multiMediaFileIdentifier or empty string",
    "multimedia_url_expiration": "multimediaExpirationTime or empty string",
    "room": "username of the person to chat with",
}
```
- **Additional Description**  

    **Case 1: User sends text message only (no multimedia)**

    The fields `multimedia_url`, `file_identifier`, and `multimedia_url_expiration` will be set to an empty string.

    **Case 2: User attaches multimedia to text message**
      
    In order to set the values for the three fields; `multimedia_url`, `file_identifier`, and `multimedia_url_expiration`, a post request will have to made to the following endpoint

      /api/rooms/upload

    A description of this endpoint is given  in the [API Endpoints Related to Chat](#api-endpoints-related-to-chat) section

[Back to Table of Contents](#table-of-contents)

#### **Single Conversation Based Notification Endpoint**

- ws://127.0.0.1:8000/ws/notifications/${username_of_other_person_in_conversation}/

Connection to get all unread message notifications for a single conversation

[Back to Table of Contents](#table-of-contents)

#### 1. **Consumer Emitted Single Conversation Unread Count Event**
- **Event Name**: `single_conversation_unread_count`
- **Description**: Sends the number of unread messages in a conversation
- **Payload**
```json
{
    "type": "single_conversation_unread_count",
    "unread_count": 5,   
}
```

[Back to Table of Contents](#table-of-contents)

#### 2. **Consumer Emitted Single Conversation New Message Notification Event**
- **Event Name**: `single_conversation_new_message_notification`
- **Description**: Sent when a new message is recieved in a conversation
- **Payload**
```json
{
    "type": "single_conversation_new_message_notification",
}
```

[Back to Table of Contents](#table-of-contents)

#### **All conversations based notification endpoint**

- ws://127.0.0.1:8000/ws/notifications/

Connection to get all unread messages from all the converstaions

[Back to Table of Contents](#table-of-contents)

#### 1. **Consumer Emitted All Conversations Unread Count Event**
- **Event Name**: `unread_count`
- **Description**: Sends the total number of unread messages a user has
- **Payload**
```json
{
    "type": "unread_count",
    "unread_count": 8,   
}

```

[Back to Table of Contents](#table-of-contents)

#### 2. **Consumer Emitted All Conversations New Message Notification Event**
- **Event Name**: `new_message_notification`
- **Description**: Sent when a user recieves a new message
- **Payload**
```json
{
    "type": "new_message_notification",
}
```

[Back to Table of Contents](#table-of-contents)

## API Endpoints Related to Chat

#### **1. Upload Multimedia Endpoint:**

- POST /api/rooms/upload

#### **Description**

This endpoint allows users to upload a file.

#### **Request**

- Method: POST
- Content-Type: multipart/form-data

#### **Request Body**
The request body should contain a FormData object with the file to be uploaded. The file should be appended to the form data with the key `myFile`.

Example using JavaScript FormData:

```javascript
const formData = new FormData();
formData.append("myFile", selectedFile);
```

#### **Response Body**

- file_location (string): The server-generated location where the uploaded file is stored.
- file_identifier (string): A unique identifier for the uploaded file.
- expiration_time (string): The expiration time of the uploaded file.

Example success response:
The success response vaires based on environment, as the development environment stores the file locally while production environment stores the file in AWS.  
- **Development Environment Response**
```json
{
    "file_location": "CV_James_Jack.pdf",
    "expiration_time": None,
    "file_identifier": "CV_James_Jack.pdf",
}
```

- **Production Environment Response**
```json
{
    "file_location": "AWS presigned URL",
    "expiration_time": "2023-12-27T22:15:45.277495",
    "file_identifier": "CV_James_Jack.pdf",
}
```

#### **Example Usage (JavaScript)**
```javascript
  const formData = new FormData();
  formData.append("myFile", selectedFile);

  axios.post("http://localhost:8000/api/rooms/upload", formData)
      .then((res) => {
          // Insert your code here
      })
      .catch((error) => {
          // Insert your code here
      });
```

[Back to Table of Contents](#table-of-contents)

#### **2. Check URL Validity Endpoint**

- GET /api/rooms/check-url/?message_id=${message_id}

#### **Description**

This endpoint is used for multimedia files stored in AWS S3

It is used to check if the AWS presigned url of a file has expired. A file is linked to a specific message, hence `message_id` is required to retrieve the file.

#### **Request**

- Method: GET

#### **Parameters**

`message_id` (required): The identifier of the message.

#### **Response Body**
```json
{
  "refresh_url": true,
}
```

If this endpoint is called in development mode `refresh_url` will return `false`.

#### **Example Usage (JavaScript)**
```javascript
  axios.get('http://127.0.0.1:8000/api/rooms/check-url/', {
    params: {
      message_id: 123
    }
  })
  .then(response => {
    // Insert your code here
  })
  .catch(error => {
    // Insert your code here
  });
```

[Back to Table of Contents](#table-of-contents)

#### **3. Refresh URL Endpoint**
- GET /api/rooms/refresh-url/?message_id=${message_id}

#### **Description**

This endpoint is used for multimedia files stored in AWS S3

Refresh the AWS presigned URL associated with a file. A file is linked to a specific message, hence `message_id` is required to retrieve the file.

#### **Request**

- Method: GET

#### **Parameters**

- `message_id` (required): The identifier of the message.

#### **Response Body**
```json
{
  "file_location": "refreshed_multimedia_url"
}
```

#### **Example Usage (JavaScript)**
```javascript
axios.get('http://127.0.0.1:8000/api/rooms/refresh-url/', {
  params: {
    message_id: 123
  }
})
  .then(response => {
    // Insert your code here
  })
  .catch(error => {
    // Insert your code here
  });
```

[Back to Table of Contents](#table-of-contents)

#### **4.Get all Conversations of a User**

- GET /api/conversations

#### **Description**

Gets a list of all the conversations a user has previously made

#### **Request**

- Method: GET

#### **Response Body**
```json
[
  {
      "id": 67,
      "name": "name of the room were the two users are assigned",
      "other_user": {
          "url": "http://127.0.0.1:8000/api/userauth/users/4/",
          "username": "other user username",
          "email": "other user email",
          "groups": ["url of group"],
          "is_active": true
      },
      "last_message": {
          "id": 565,
          "from_user": {
              "url": "http://127.0.0.1:8000/api/userauth/users/2/",
              "username": "sender username",
              "email": "sender email",
              "groups": ["url of group"],
              "is_active": true
          },
          "to_user": {
              "url": "http://127.0.0.1:8000/api/userauth/users/4/",
              "username": "receiver username",
              "email": "reciever email",
              "groups": ["url of group"],
              "is_active": true
          },
          "date_added": "2023-12-26T21:43:30.597375Z",
          "content": "last message",
          "multimedia_url": "url of multimedia file"
      }
  }
]
```

[Back to Table of Contents](#table-of-contents)

#### **Example Usage (JavaScript)**

```javascript
try {
    const response = await axios.get('http://127.0.0.1:8000/api/conversations', {
      headers: {
        Authorization: "access token",
      },
    });

    const data = response.data;
    // Insert your code here
  } catch (error) {
    console.error('Error fetching users:', error);
  }
```

[Back to Table of Contents](#table-of-contents)

#### **5.Get all Conversations within a Room**

- GET /api/rooms/${room}/messages

#### **Description**

Gets a all converastions within a room (all conversations a user has with another user).
The variable `room` is the username of the other person in the conversation.

#### **Request**

- Method: GET

#### **Response Body**
```json
{
    "messages": [
        {
            "id": 298,
            "from_user": {
                "url": "http://127.0.0.1:8000/api/userauth/users/2/",
                "username": "sender username",
                "email": "sender email",
                "groups": ["url of group"],
                "is_active": true
            },
            "to_user": {
                "url": "http://127.0.0.1:8000/api/userauth/users/4/",
                "username": "reciever username",
                "email": "receiver email",
                "groups": ["url of group"],
                "is_active": true
            },
            "date_added": "2023-10-26T07:24:29.296910Z",
            "content": "message"
        }
  ]
}
```

#### **Example Usage (JavaScript)**

```javascript
  try {
    const response = await axios({
        method: "get",
        url: `http://127.0.0.1:8000/api/rooms/${room}/messages`,
        headers: {
            Authorization: "access token",
        },
    })

    const data = response.data;

    // Insert your code here
  
  } catch (error) {
      console.log("Error: ", error)
  }
```

[Back to Table of Contents](#table-of-contents)
