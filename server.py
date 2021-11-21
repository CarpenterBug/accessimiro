import json
import os
import ffmpeg
from pydub import AudioSegment


from flask import Flask, request, send_from_directory
from werkzeug.datastructures import FileStorage
from wit import Wit
# import magic

from interaction import classify

WIT_API_KEY = "TAS4VSQRWLVL554LN3TCXJQUXQ7ABMAL"
client = Wit(WIT_API_KEY)
app = Flask(__name__)


@app.route('/test')
def test():
    q = request.values['q']
    res = client.message(q)
    classify(res)

    return 'success'


@app.route('/submit', methods=['POST'])
def submit():
    try:
        # f = request.files['audio']
        f = request.files['file']
    except Exception as e:
        print(e)
        return 'vittu'

    name = f.filename
    print('got a file,', name)

    # os.remove(name)
    f.save('audio.wav')

    # stream = ffmpeg.input(name)
    # audio = stream.audio
    # stream = ffmpeg.output(audio, 'audio.mp3')
    # ffmpeg.run(stream)

    # sound = AudioSegment.from_file('audio.webm', format='webm')
    # sound.export('audio.mp3', format="mp3")

    # stream = ffmpeg.input(name)
    # stream = ffmpeg.output(stream, name)
    # ffmpeg.run(stream)

    # mime = magic.from_file(name, mime=True)

    # if mime == 'audio/mpeg':
    #     mime = 'audio/mpeg3'

    with open('audio.wav', 'rb') as b:
        # print(mime)  # wrong
        try:
            res = client.speech(b, {'Content-Type': 'audio/wav'})

            result = {'action_required': False}

            s = classify(res)
            if s:
                result['action_required'] = True
                result['text'] = s
            else:
                result['text'] = res['text']

            result['intent_recognized'] = res['intents'] == []

            return json.dumps(result)
        except Exception as e:
            print(e)
            return 'perkele'


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
