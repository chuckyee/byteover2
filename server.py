import requests
import json
import io
import shutil
from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import Record, VoiceResponse
from twilio.rest import Client

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

@app.route('/record_action', methods=['POST'])
def handle_record_action():
    print("Handling record action callback.")
    url = request.form.get("RecordingUrl") + ".mp3"
    filename = "/tmp/{}".format(url.split('/')[-1]) # get unique filename
    r = requests.get(url)
    with open(filename, 'wb') as f:
        shutil.copyfileobj(io.BytesIO(r.content), f)
        print("Wrote mp3 out to file {}".format(filename))
    return "Hello"

@app.route('/voice', methods=['GET', 'POST'])
def handle_voice():
    """Handle incoming voice calls."""
    response = VoiceResponse()
    response.say("Hello human.")
    response.record(timeout=3, transcribe=True, action='/record_action')
    response.say("Thanks. Goodbye.")
    response.hangup()
    print(response)
    return str(response)

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
    #account_sid = "ACc1ae6b931a01753024331e505977abcc"
    #auth_token = 
    client = Client(account_sid, auth_token)
