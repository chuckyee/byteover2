from flask import Flask
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_get():
    pass

@app.route('/', methods=['POST'])
def handle_post():
    """Respond to incoming calls with a simple text message."""

    resp = MessagingResponse().message("Hello, Mobile Monkey")
    return str(resp)

if __name__ == '__main__':
    app.config.from_pyfile('config')
    app.run(port=int(app.config['PORT']), debug=True)
