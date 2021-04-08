from google_trans_new import google_translator
from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
from gtts import gTTS
from langdetect import detect, DetectorFactory

# from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
# API = Api(app)


# class Translator(Resource):
#     @staticmethod
#     def post():
#         parser = reqparse.RequestParser()
#         parser.add_argument('text', default='')

#         args = parser.parse_args()  # dict

#         sentence = args['text']

#         translator = google_translator()
#         trans_sentence = translator.translate(sentence, lang_tgt='vi')

#         # print(trans_sentence)

#         output = {'translated_text': trans_sentence}

#         return output, 200


# API.add_resource(Translator, '/translate')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json(force=True)
    sentence = data['text']

    translator = google_translator()
    trans_sentence = translator.translate(sentence, lang_tgt='vi')

    # print(trans_sentence)

    output = {'translated_text': trans_sentence}

    return jsonify(output)


@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json(force=True)
    sentence = data['text']
    filename = data['name'] + '.mp3'
    robot = gTTS(sentence, lang='vi', tld='com.vn')
    robot.save('tmp/' + filename)

    output = {
        "url": url_for('speak_file', filename=filename)
    }

    return jsonify(output)


@app.route('/detect', methods=['POST'])
def detect_language():
    data = request.get_json(force=True)
    sentence = data['text']

    DetectorFactory.seed = 0
    output = {"lang": detect(sentence)}

    return jsonify(output)


@app.route('/speak_files/<filename>')
def speak_file(filename):
    return send_from_directory('tmp', filename)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
