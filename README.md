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

# Endpoints

## users/register

## users/login

## messaging/api
Root url for the message related endpoints.

## messaging/api/message
**Allowed methods**: [GET, POST]

**GET**
List all messages sent by the requesting user.

**POST**
Creates a message objects and sends to user.

## messaging/api/conversation
**Allowed methods**: [GET]

**GET**
List all users that requesting user has texted or has been texted.

## messaging/api/conversation/<username>
**Allowed methods**: [GET]

**GET**
List all messages between the requesting user and user with the url param <username>

## messaging/api/conversation/<username>/send_message
**Allowed methods**: [POST]

**POST**
Send a message to user with the <username>

## messaging/api/blackist


License
----

MIT

