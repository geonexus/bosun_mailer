__author__ = 'gjp'
from flask import Flask, json, request, Response
from flask.ext.mail import Mail, Message
import httplib


app =Flask(__name__)
mail=Mail(app)

app.config['MAIL_SERVER']='mail.server.org'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail=Mail(app)

content_type = 'application/json'


@app.route("/", methods=['POST'])
def index():
    try:
        bosun_json = json.loads(request.data)
    except ValueError:
        # Data is not a well-formed json
        message = "[{}] received {} from ip {}:{}"\
            .format("-", json, request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT'])

        return Response(response="{\"error\":\"Bad request. The payload is not well-defined json format\"}\n",
                        status=httplib.BAD_REQUEST,
                        content_type=content_type)
    email = request.json['email']
    body = request.json['description']

    msg = Message(
              'Bosun mailer',
    sender='bosun-notification@imdea.org',
    recipients=[email])
    msg.body = body
    try:
        mail.send(msg)
    except Exception as ex:
        print ex.message
    return "Sent"

if __name__ == "__main__":
    app.run(port=81)