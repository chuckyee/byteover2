import requests
import json
import io
import shutil
from flask import Flask, Response, request

from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import Record, VoiceResponse

from azure import askazure
import audio


app = Flask(__name__)


def analyze_sentiment(text):
    """Analyze sentiment of passed string

    Returns: json Azure sentiment object
    """
    key = app.config['AZURE_SUBSCRIPTION_KEY']
    sentiment = askazure.askazure(text, key)
    score = sentiment['documents'][0]['score']
    return score


@app.route('/transcribe_action', methods=['POST'])
def handle_transcribe_action():
    print("Handling transcribe action callback")
    text = request.form.get("TranscriptionText")
    return 0


@app.route('/music/<audiofile>', methods=['GET'])
def handle_audiofile_get(audiofile):
    filename = "/tmp/response_{}.wav".format(audiofile)
    print("Serving file {}".format(filename))
    with open(filename, 'rb') as f:
        audio_data = f.read()
    return Response(audio_data, mimetype="audio/wav")


@app.route('/record_action', methods=['POST'])
def handle_record_action():
    print("Handling record action callback.")
    audio_format = ".mp3"
    url = request.form.get("RecordingUrl")
    basename = url.split('/')[-1] # get unique filename
    filename = "/tmp/{}{}".format(basename, audio_format)
    r = requests.get(url + audio_format)
    with open(filename, 'wb') as f:
        shutil.copyfileobj(io.BytesIO(r.content), f)
        print("Wrote mp3 out to file {}".format(filename))

    filename_happy_music = './music/brandenburg.wav'
    outputfile = "/tmp/response_{}.wav".format(basename)
    audio.mixing_librosa(filename, filename_happy_music, outputfile)
    audio_endpoint = "{}/music/{}".format(app.config['PUBLIC_URL'], basename)
    response = VoiceResponse()
    response.play(audio_endpoint)
    response.say("Thanks. Goodbye.")
    response.hangup()
    return str(response)


@app.route('/voice', methods=['GET', 'POST'])
def handle_voice():
    """Handle incoming voice calls."""
    response = VoiceResponse()
    response.say("Record a message and stay on the line when finished.")
    response.record(timeout=2, action='/record_action')
    print(response)
    return str(response)


@app.route('/sms', methods=['GET', 'POST'])
def handle_sms():
    """Respond to incoming SMS with a simple text message."""
    print(request.values)
    body = request.values.get("Body")

    score = analyze_sentiment(body)
    print(score)

    if score < 0.33333:
        text = "Dude, lighten the f- up."
    elif score < 0.66666:
        text = "You seem neither here nor there."
    else:
        text = "Stop farting rainbows and unicorns."

    resp = MessagingResponse()
    resp.message(text)
    return str(resp)


if __name__ == '__main__':
    app.config.from_pyfile('config')
    app.run(port=int(app.config['PORT']), debug=True)
