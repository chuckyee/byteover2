#!/usr/bin/python3
""" Module to perform azure queries. I am not concerned about
security, so may be vulnerable to sql injections, bla bla bla
"""

import logging
import requests

AZUREKEY = 'PUT-YOUR-KEY-HERE'

def askazure(text):
    """Perform a sentiment analysis request using azure service
    """

    header = {'Ocp-Apim-Subscription-Key': AZUREKEY,
              'Content-Type': 'application/json',
              'Accept': 'application/json'}
    data = { "documents":
            [ {"language": "en",
               "id": "1",
               "text":text}
             ] }

    url = '''https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'''
    response = requests.post(url, headers=header, json=data)
    return response.text

def main():
    text = "That s awesome."
    result = askazure(text)
    print(result)

if __name__ == "__main__":
    main()


