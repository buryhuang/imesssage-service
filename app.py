from flask import Flask
from flask import request

import os

app = Flask(__name__)


@app.route('/imessage', methods = ['GET', 'POST'])
def handle_imesssage():
    result = 167
    if request.method == 'POST':
        data = request.form
        print("sending %s to %s" % (data.get('video-url'), data.get('receiver_number')))
        result = os.system('/usr/bin/osascript -e \'tell application \"Messages\" to send \"From Bury %s\" to buddy \"%s\" of service \"SMS\"\'' % (data.get('video-url'), data.get('receiver_number')))
    return "Executed! with %d" % result

if __name__ == '__main__':
    app.run()
