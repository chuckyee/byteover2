from flask import Flask
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_get():
    pass

@app.route('/sms', methods=['GET', 'POST'])
def handle_sms():
    """Respond to incoming SMS with a simple text message."""

    resp = MessagingResponse().message("Hello, puny human.")
    return str(resp)

if __name__ == '__main__':
    app.config.from_pyfile('config')
    app.run(port=int(app.config['PORT']), debug=True)
