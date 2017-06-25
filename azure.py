#!/usr/bin/python3
""" Module to perform azure queries. I am not concerned about
security, so may be vulnerable to sql injections, bla bla bla
"""

import logging
import requests
import json
from subprocess import Popen, PIPE

def text_to_sentiment(text, key):
    """Perform a sentiment analysis request using azure service
    """

    header = {'Ocp-Apim-Subscription-Key': key,
              'Content-Type': 'application/json',
              'Accept': 'application/json'}
    data = { "documents":
            [ {"language": "en",
               "id": "1",
               "text":text}
             ] }

    url = '''https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'''
    response = requests.post(url, headers=header, json=data)
    return json.loads(response.text)

def wav_to_text(wavfile, requestid, jwt):
    """Extract text from wave file
    """
    cmd = '''curl  -X POST 'https://speech.platform.bing.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US&locale=en-US&format=simple&requestid={}' -H 'Transfer-Encoding: chunked'  -H 'Authorization: Bearer {}' -H 'Content-type: audio/wav; codec="audio/pcm"; samplerate=8000' --data-binary @'{}' '''.format(requestid, jwt, wavfile)

    process = Popen([cmd], stdout=PIPE, shell=True)
    (output, err) = process.communicate()
    exit_code = process.wait()
    result = json.loads(output.decode('ascii'))
    return result['DisplayText']

def main():
    #text = "That s awesome."
    #result = askazure(text)
    #print(result)

    wavfile = 'data/speech.wav'
    result = wav_to_text(wavfile)
    print(result)

if __name__ == "__main__":
    main()


