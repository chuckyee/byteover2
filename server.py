import requests
import json
import io
import shutil
import time

from flask import Flask, Response, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import Record, VoiceResponse

import azure
import audio

app = Flask(__name__)


def analyze_sentiment(text):
    """Analyze sentiment of passed string
    """
    key = app.config['AZURE_SUBSCRIPTION_KEY']
    sentiment = azure.text_to_sentiment(text, key)
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


@app.route('/recording_status', methods=['POST'])
def handle_recording_status():
    print("Handling recording status callback.")
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


@app.route('/record_action', methods=['POST'])
def handle_record_action():
    print("Handling record action callback.")

    # Generate temporary filename to store mp3 recording
    audio_format = ".mp3"
    url = request.form.get("RecordingUrl")
    basename = url.split('/')[-1] # get unique filename
    mp3_filename = "/tmp/{}{}".format(basename, audio_format)

    # download recording from Twilio and write to file
    time.sleep(0.5)
    r = requests.get(url + audio_format)
    with open(mp3_filename, 'wb') as f:
        shutil.copyfileobj(io.BytesIO(r.content), f)
        print("Wrote mp3 out to file {}".format(mp3_filename))

    # convert mp3 file to wav file, then use Azure's speech to text
    wav_filename = "/tmp/{}.wav".format(basename)
    audio.mp3_to_wav(mp3_filename, wav_filename)
    text = azure.wav_to_text(wav_filename, app.config['AZURE_REQUEST_ID'], app.config['AZURE_JWT'])
    print("Azure speech to text returned: {}".format(text))

    # analyze sentiment
    sentiment = analyze_sentiment(text)
    print("Sentiment score is: {}".format(sentiment))

    # select music based on sentiment
    if sentiment <= 0.5:
        background_music = './music/imperial-march-quieter.wav'
    else:
        background_music = './music/brandenburg.wav'

    # mix background music into call audio
    outputfile = "/tmp/response_{}.wav".format(basename)
    audio.mixing_librosa(wav_filename, background_music, outputfile)

    # setup response to play file
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
    response.record(timeout=2, action='/record_action', recordingStatusCallback='/recording_status')
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
