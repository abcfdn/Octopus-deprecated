 #Octopus (章鱼烧)

## Motivation
[![Build Status/.org](https://travis-ci.org/abcfdn/Octopus.svg?branch=master)](https://travis-ci.org/abcfdn/Octopus)
[![Build Status/.com](https://travis-ci.com/abcfdn/Octopus.svg?branch=master)](https://travis-ci.com/abcfdn/Octopus)
Note: Travis-CI.org is migrating to Travis-CI.com, remove .org status when needed.

A content CI/CD (continues integration/delivery) management application for ABC Blockchain Community

## Features
1. In one click (a buttom click or command line input), Octopus can delivers event/media content to supported media platforms as desired.
2. Content monitoring/filtering in Slack/Discord/Telegram using chatbot.

## Supported Platforms

### Google Drive

- Read
- Download
- Upload

Image

- Download
- Upload

### Meet Up

- Create Event
- Update Event
- Delete Event

### Eventbrite

- Create Event
- Update Event
- Delete Event

### Email List

- generate template
- manage attachment
- send to email list

### Discord

### WeChat Group

### WeChat Official Account

### Telegram

### Twitter

### Facebook Page

### Slack

## Runbook

Start Mongo
```
mongod --dbpath /root/data/mongodb --auth --port 27017

FLASK_APP=$PWD/app/http/api/endpoints.py FLASK_ENV=development pipenv run python -m flask run --port 4433 --host 0.0.0.0

npm start
```
