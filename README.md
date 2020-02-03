# brightwheel Email Service Exercise
Send email through POST request by way of either MailGun or Sendgrid
# Overview
## Setup
Clone repo from Github repo

Must have `Docker` installed on machine (either for Mac or Windows)

Once `Docker` installed and app launched, open terminal and in directory run:

`docker-compose up`

Use your api testing client of choice (e.g. PostMan) and send a POST request to `'http://localhost:5000/email'`

## Technology Used

`Docker`

Docker allows the ability to provide a more consistent deployment accross any machine that might want to run my API service

`Flask`

`Flask-Restful`

Simple Flask application with extension of Flask-Restful to build this REST API with a more object oriented HTTP method setup

## Retro - After implementation

If I were to spend more time on this project, I would integrate the Marshmallow library that facilitates and provides more robust validation of input payloads to the API. 

Would also have more adequate unit testing, along with extending the ones currently present.

If the API were to be extended, proper directory organization for future expansion.

## Sending an Email
**Endpoint Definition** <br />
 
 `POST /email`

**Parameters**

 All fields required.

 `”to” type: string`  
    * the email address to send to

 `”to_name” type: string`<br />
    * the name to accompany the email

 `”from” type: string`<br />
    * the email address in the from and reply fields

 `”from_name” type: string`<br />
    * the name to accompany the from/reply emails

 `”subject” type: string`<br />
    * the subject line of the email

 `”body” type: string`<br />
    * the HTML body of the email

**Example Payload**

`{
"to": "fake@fake.com",
"to_name": "Mr. Fake",
"from": "noreply@mybrightwheel.com", "from_name": "Brightwheel",
"subject": "A Message from Brighwheet", "body": "<h1>Your Bill</h><p>$10</p>"
}`

**Response**<br />

`200 OK` <br />
* data validated and sent through to email service

`400 Bad Request` <br />
{error message with incorrect input data}