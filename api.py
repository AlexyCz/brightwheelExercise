# frameworks
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import requests
import markdown
import os
import re
import config as cfg


# instance of Flask created
app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
# api created
api = Api(app)

@app.route('/')
def index():
    with open(os.path.dirname(app.root_path) +
              '/app/README.md', 'r') as mdFile:
        return markdown.markdown(mdFile.read())


class Email(Resource):
    def post(self):
        def send_simple_message(args):
            # config check to see which service to use
            if cfg.emailService == 'mailgun':
                """ MailGun and Sendgrid API Keys can be changed in the config file"""
                response = requests.post(
                    "https://api.mailgun.net/v3/{}/messages".format(cfg.domains['MAILGUN_DOMAIN']),
                    auth=("api", cfg.apiKeys['MAILGUN_API_KEY']),
                    data={"from": "{} <{}>".format(args['from_name'], args['from']),
                          "to": [args['to'], args['to_name']],
                          "subject": args['subject'],
                          "text": args['body']})
                return (response.json(), response.status_code)

            elif cfg.emailService == 'sendgrid':
                message = Mail(
                    from_email=args['from'],
                    to_emails=args['to'],
                    subject=args['subject'],
                    html_content=args['body'])

                try:
                    sg = SendGridAPIClient(cfg.apiKeys['SENDGRID_API_KEY'])
                    response = sg.send(message)
                    return (response.body, response.status_code)

                except Exception as e:
                    return(e.message, 400)

        # parse all arguments passed in with request; requirements set
        parser = reqparse.RequestParser()
        parser.add_argument('to', type=str, required=True)
        parser.add_argument('to_name', type=str, required=True)
        parser.add_argument('from', type=str, required=True)
        parser.add_argument('from_name', type=str, required=True)
        parser.add_argument('subject', type=str, required=True)
        parser.add_argument('body', type=str, required=True)
        data = parser.parse_args()

        # HTML data processing
        data['body'] = 'Hello {}, \n {}'.format(data['to_name'], data['body'])
        data['body'] = re.sub(r'<[^>]+?>', ' ', data['body'])

        # all passed -> send email
        return send_simple_message(data)


api.add_resource(Email, '/email')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
