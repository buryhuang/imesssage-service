from flask import Flask
from flask import request

import os

app = Flask(__name__)

def generate_send_script(app_number, to_number, msg):
    f = open("send_message.applescript", "w")
    f.write("tell application \"Messages\"\n")
    f.write("    if not running then run\n")
    f.write("    activate\n")
    f.write("    set theBuddy1 to buddy \"%s\" of service \"SMS\"\n" % to_number)
    f.write("    set theBuddy2 to buddy \"%s\" of service \"SMS\"\n" % app_number)
    f.write("    set thisChat to make new text chat with properties {participants:{theBuddy1, theBuddy2}}\n")
    f.write("    set thisMessage to send \"%s\" to thisChat\n" % msg)
    f.write("end tell\n")
    f.close

@app.route('/imessage', methods = ['GET', 'POST'])
def handle_imesssage():
    result = 167
    if request.method == 'POST':
        data = request.form
        print("sending %s to %s" % (data.get('video-url'), data.get('receiver_number')))
        generate_send_script("+12038942437", data.get('receiver_number'), data.get('msg'))
        result = os.system('/usr/bin/osascript send_message.applescript')
        print("executed with return %d" % result)
        if result != 0:
            print("Failed to send as SMS, trying to send as iMessage")
            result = os.system('/usr/bin/osascript -e \'tell application \"Messages\" to send \"%s\" to buddy \"%s\" of service \"SMS\"\'' % (data.get('msg'), data.get('receiver_number')))
            print("executed with return %d" % result)

    return "Executed! with %d" % result

if __name__ == '__main__':
    app.run()
