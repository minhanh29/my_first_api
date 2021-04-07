from google_trans_new import google_translator
from flask import Flask
from flask_restful import Api, Resource, reqparse


APP = Flask(__name__)
API = Api(APP)


class Translator(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('text', default='')

        args = parser.parse_args()  # dict

        sentence = args['text']

        translator = google_translator()
        trans_sentence = translator.translate(sentence, lang_tgt='vi')

        print(trans_sentence)

        output = {'translated_text': trans_sentence}

        return output, 200


API.add_resource(Translator, '/translate')

if __name__ == '__main__':
    APP.run(debug=True, port='8080')
