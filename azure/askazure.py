#!/usr/bin/python3
""" Module to perform azure queries. I am not concerned about
security, so may be vulnerable to sql injections, bla bla bla
"""

import logging

AZUREKEY = 'PUT YOUR KEY HERE'

def main():
    cmd = '''curl -H "Ocp-Apim-Subscription-Key: {}" -H "Content-Type: application/json" -H  "Accept: application/json" -X POST -d '{     "documents": [         {             "language": "en",             "id": "1",             "text": "That s awesome."         }     ] } ' https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'''.format(AZUREKEY)

if __name__ == "__main__":
    main()


