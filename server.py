from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json
from azure import askazure

app = Flask(__name__)


def analyze_sentiment(text):
    """Analyze sentiment of passed string

    Returns: json Azure sentiment object
    """
    key = app.config['AZURE_SUBSCRIPTION_KEY']
    sentiment = askazure.askazure(text, key)
    score = sentiment['documents'][0]['score']
    return score

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

    score = analyze_sentiment(body)
    print(score)

    text = "Puny human, '{} in bed with cats' to you too. Your level of positivity is {}".format(body, score)
    resp = MessagingResponse().message(text)
    return str(resp)

if __name__ == '__main__':
    app.config.from_pyfile('config')
    app.run(port=int(app.config['PORT']), debug=True)
