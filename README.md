
# MessageService
MessageService is a self contained web service utilizing rest api concepts. You can register users, login and users can send messages or block each other. MessageService uses postgres as database and django as the backend framework. It runs in docker.

## Requirements

MessageService is developed and tested with docker and docker-compose. Hence only requirements are;

    - Docker
    - Docker Compose


## Installation and Setup
Clone github repo and build images;

```sh
$ git clone https://github.com/thetarby/message-service.git
$ cd message-service
$ docker-compose up
```
As soon as docker containers are up and running, MessageService starts to run on localhost:8000. It has a browsable api too so that you can check it out and try from browser.

## About Rest Api
MessageService has a browsable api which means you can
- go to `http://localhost:8000/messaging/api` in your browser
- click login button at the top right corner of the page
- type your credentials
- and start to use messaging functionality by following self-explaining hyperlinks

MessageService obeys rest api standards hence all successful requests responds with an appropriate http status, so is all unsuccesful requests with an explanation of the error in response body. It utilizes http methods with their meanings and uses json data format for requests and responses.

MessageService supports two different authentication schemes.
- Session Authentication: Used to authenticate in browsable api.
- Token Authentication: For all other use cases
Session authentication works with cookies. When you login from browser all necessary fields are set in cookies and sent to server at each request.

Token authentication is for all other use cases. A post request with username and password to `/users/login` will return a token. That token should be added to Authorization header with a 'Token ' prefix (such as `Token aaabbb111bbbccc`) should be added to all requests that requires authentication. 

When a request is made, MessageService checks whether needed fields are set in the cookies for session authentication. If they are set, session authentication scheme is used otherwise token authentication is used.

If a request is unsuccessful response body includes a message about it. If error is about a field in request body message would be in the format;
```json
{'field_name':'error', 'other_field':'error'...}
``` 
If error is not about a field;
```json
{'non_field_error':'error'...}
``` 

# Endpoints


## Register New User
----
Create new user.

* **URL:**
/users/register/

* **Method:**

  `POST`
  

* **Request Body**
    ```JSON
  {
      "username":"some_username",
      "password":"some_password",
      "password_again":"some_password",
      "email_address":"example@example.com"
  }
    ```
* **Success Response:**

    **Code:** `201 CREATED`
    **Content:** `{ "username" : "some_username" }`
 
* **Error Response:**

    **Code:** `400 BAD REQUEST` 
    **Content:** `{ "field" : "error" }`

  OR

    **Code:** `401 UNAUTHORIZED`
    **Content:** `{ "detail": "error" }`

* **Sample Curl Call:**

  ```shell
    curl --location --request POST 'http://localhost:8000/users/register/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "username":"user",
        "password":"tarba12345",
        "password_again":"tarba12345"
    }'
  ```

## Login
----
Returns an authentication token for the given user.

* **URL:**
/users/login/

* **Method:**

  `POST`
  

* **Request Body**
    ```JSON
    {
        "username":"user",
        "password":"tarba12345"
    }
    ```
* **Success Response:**

    **Code:** `200 OK`
    **Content:** `{ "token" : "some-token" }`
 
* **Error Response:**

    **Code:** `400 BAD REQUEST` 
    **Content:** `{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}`


* **Sample Curl Call:**

  ```shell
    curl --location --request POST 'http://localhost:8000/users/login/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "username":"user12",
        "password":"tarba12345"
    }'
  ```


## List Messages
----
Lists both received and sent messages of the user

* **URL:**
/messaging/api/message

* **Method:**

  `GET`
  
* **Success Response:**

    **Code:** `200 OK`
    **Content:**
    ```json
    [
        {
            "from_user": "thetarby",
            "to_user": "mehmet",
            "content": "selam",
            "sent_date": "2020-10-20T16:32:59.648124Z"
        },
        {
            "from_user": "user",
            "to_user": "thetarby",
            "content": "naber",
            "sent_date": "2020-10-20T16:34:00.579420Z"
        }
    ]
    ```
 
* **Error Response:**

    **Code:** `401 UNAUTHORIZED`
    **Content:** `{
        "detail": "Authentication credentials were not provided."
    }`



* **Sample Curl Call:**

  ```shell
    curl --location --request GET 'http://localhost:8000/messaging/api/conversation' \
    --header 'Authorization: Token c842119167194f5a3a2ab781882aa744357c6727'
  ```


## Send Message With Username
----
Send a message to any user by giving username parameter in request body.

* **URL:**
/messaging/api/message

* **Method:**

  `POST`
* **Request Body:**
	```json
	{
	"to_user":"username",
	"content":"naber"
	}
	```

* **Authentication:**
  Required.
	- TokenAuthentication
	- SessionAuthentication
  
* **Success Response:**

    **Code:** `201 CREATED`
    **Content:**
    ```json
	{
	"message": "naber",
	"created_at": "2020-10-21T21:09:24.877370Z"
	}
    ```
 
* **Error Response:**

    **Code:** `401 UNAUTHORIZED`
    **Content:** `{
        "detail": "Authentication credentials were not provided."
    }`



* **Sample Curl Call:**

  ```shell
	curl --location --request POST 'http://localhost:8000/messaging/api/message' \
	--header 'Authorization: Token c842119167194f5a3a2ab781882aa744357c6727' \
	--header 'Content-Type: application/json' \
	--data-raw '{
	"to_user":"thetarbyy",
	"content":"naber"
	}'
  ```




## List Conversations With Other Users
----
List hyperlinks to conversations with other users

* **URL:**
/messaging/api/conversation/

* **Method:**

  `GET`

* **Authentication:**
  Required.
	- TokenAuthentication
	- SessionAuthentication
  
* **Success Response:**

    **Code:** `200 OK`
    **Content:**
    ```json
	[
	{
	"conversation": "http://localhost:8000/messaging/api/conversation/thetarby"
	},
	{
	"conversation": "http://localhost:8000/messaging/api/conversation/gozde"
	}
	]
    ```
 
* **Error Response:**

    **Code:** `401 UNAUTHORIZED`
    **Content:** `{
        "detail": "Authentication credentials were not provided."
    }`



* **Sample Curl Call:**

  ```shell
	curl --location --request GET 'http://localhost:8000/messaging/api/conversation' \
	--header 'Authorization: Token c842119167194f5a3a2ab781882aa744357c6727'
  ```





## List Messages In a Conversation
----
List both received and sent messages between a user and requesting user

* **URL:**
/messaging/api/conversation/:username/

* **URL Parameters:**
`username` is the username attribute of the other user.

* **Method:**
  `GET`
  
* **Authentication:**
  Required.
	- TokenAuthentication
	- SessionAuthentication
  
* **Success Response:**

    **Code:** `200 OK`
    **Content:**
    ```json
	[
	{
	"from_user": 14,
	"to_user": 1,
	"content": "naber",
	"sent_date": "2020-10-20T13:18:25.879392Z"
	},
	{
	"from_user": 1,
	"to_user": 14,
	"content": "iyi senden naber",
	"sent_date": "2020-10-20T13:20:08.020181Z"

	},
	]
    ```
 
* **Error Response:**

    **Code:** `401 UNAUTHORIZED`
    **Content:** `{
        "detail": "Authentication credentials were not provided."
    }`



* **Sample Curl Call:**

  ```shell
	curl --location --request GET 'http://localhost:8000/messaging/api/conversation/thetarby' \
	--header 'Authorization: Token c842119167194f5a3a2ab781882aa744357c6727'
  ```






## Send Message to a Conversation
----
This endpoint is very similar to `Send Message`. This time only username is used as a url parameter hence only content parameter is passed in request body.

* **URL:**
/messaging/api/conversation/:username/send_message

* **URL Parameters:**
`username` is the username attribute of the other user.

* **Method:**
  `POST`
  
 * **Request Body:**
	```json
	{
	"content":"naber"
	}
	```
* **Authentication:**
  Required.
	- TokenAuthentication
	- SessionAuthentication
  
* **Success Response:**

    **Code:** `201 CREATED`
    **Content:**
    ```json
	{
	"message": "naber",
	"created_at": "2020-10-21T21:22:15.525762Z"
	}
    ```
 
* **Error Response:**

    **Code:** `401 UNAUTHORIZED`
    **Content:** `{
        "detail": "Authentication credentials were not provided."
    }`



* **Sample Curl Call:**

  ```shell
	curl --location --request POST 'http://localhost:8000/messaging/api/conversation/thetarby/send_message' \
	--header 'Authorization: Token c842119167194f5a3a2ab781882aa744357c6727' \
	--header 'Content-Type: application/json' \
	--data-raw '{
	"content":"naber"
	}'
  ```





## List Blacklisted Users
----
List users who are blocked by the requesting user.

* **URL:**
/messaging/api/blacklist

* **Method:**
  `GET`
  
* **Authentication:**
  Required.
	- TokenAuthentication
	- SessionAuthentication
  
* **Success Response:**

    **Code:** `200 OK`
    **Content:**
    ```json
	[
	{
	"blocked_user": "user",
	"detail": "http://localhost:8000/messaging/api/blacklist/user"
	}
	]
    ```
 
* **Error Response:**

    **Code:** `401 UNAUTHORIZED`
    **Content:** `{
        "detail": "Authentication credentials were not provided."
    }`



* **Sample Curl Call:**

  ```shell
	curl --location --request GET 'http://localhost:8000/messaging/api/blacklist' \
	--header 'Authorization: Token c842119167194f5a3a2ab781882aa744357c6727' \
	--data-raw ''
  ```








## Blacklist a User
----
Blocks a user from sending more messages to the requesting user.

* **URL:**
/messaging/api/blacklist

* **Method:**
  `POST`
  
 * **Request Body:**
	```json
	{
	"blocked_user":"username"
	}
	```
* **Authentication:**
  Required.
	- TokenAuthentication
	- SessionAuthentication
  
* **Success Response:**

    **Code:** `201 CREATED`
    **Content:**
    ```json
	{
	"blocked_user": "username",
	"detail": "http://localhost:8000/messaging/api/blacklist/username"
	}
    ```
 
* **Error Response:**

    **Code:** `401 UNAUTHORIZED`
    **Content:** `{
        "detail": "Authentication credentials were not provided."
    }`



* **Sample Curl Call:**

  ```shell
	curl --location --request POST 'http://localhost:8000/messaging/api/blacklist' \
	--header 'Authorization: Token c842119167194f5a3a2ab781882aa744357c6727' \
	--header 'Content-Type: application/json' \
	--data-raw '{
	"blocked_user":"user"
	}'
  ```




## Remove a User From Blacklisted Users
----
Unblocks a user.

* **URL:**
/messaging/api/blacklist/:username

* **URL Parameters:**
`username` is the username attribute of the user whose block will be removed.

* **Method:**
  `DELETE`
  
* **Authentication:**
  Required.
	- TokenAuthentication
	- SessionAuthentication
  
* **Success Response:**

    **Code:** `204 No Content`

* **Error Response:**

    **Code:** `401 UNAUTHORIZED`
    **Content:** `{
        "detail": "Authentication credentials were not provided."
    }`


* **Sample Curl Call:**

  ```shell
	curl --location --request DELETE 'http://localhost:8000/messaging/api/blacklist/user' \
	--header 'Authorization: Token c842119167194f5a3a2ab781882aa744357c6727' \
	--data-raw ''
  ```


## Display activities
----
MesageService records activities such as invalid login attempts, sending messages etc... This endpoint lists them in a human readable form.

* **URL:**
/activity/all

* **Method:**
  `GET`
  
* **Authentication:**
  Required.
	- TokenAuthentication
	- SessionAuthentication
  
* **Success Response:**

    **Code:** `200 OK`

* **Error Response:**

    **Code:** `401 UNAUTHORIZED`
    **Content:** ```json
    {
      "activities": [
          "user0 sent Message object (1) on user2 0 minutes ago"
      ]
    }
    ```


* **Sample Curl Call:**

  ```shell
	curl --location --request DELETE 'http://localhost:8000/messaging/api/blacklist/user' \
	--header 'Authorization: Token c842119167194f5a3a2ab781882aa744357c6727' \
	--data-raw ''
  ```

License
----

MIT

