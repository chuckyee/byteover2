from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)


def analyze_sentiment(text):
    """Analyze sentiment of passed string"""
    return 0

@app.route('/', methods=['GET'])
def handle_get():
    pass

@app.route('/voice', methods=['GET', 'POST'])
def handle_voice():
    """Handle incoming voice calls."""
    pass

@app.route('/sms', methods=['GET', 'POST'])
def handle_sms():
    """Respond to incoming SMS with a simple text message."""
    print(request.values)
    body = request.values.get("Body")

    sentiment = analyze_sentiment(body)
    print(sentiment)

    text = "Puny human, '{} in bed with cats' to you too.".format(body)
    resp = MessagingResponse().message(text)
    return str(resp)

if __name__ == '__main__':
    app.config.from_pyfile('config')
    app.run(port=int(app.config['PORT']), debug=True)
