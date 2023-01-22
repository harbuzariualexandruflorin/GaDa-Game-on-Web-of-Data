import waitress
from flask_restful import Api
from paste.translogger import TransLogger

from gada_api.build_controller import *
from gada_api.high_scores_controller import GADAHighScoresController
from gada_api.info_controller import GADACardsInfoController


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


def set_api_resources():
    api = Api(app)
    api.add_resource(GADACardsBuildController, '/gada_card_deck/generate')
    api.add_resource(GADACardsInfoController, '/gada_card_deck/info')
    api.add_resource(GADAHighScoresController, '/high_scores')


def start_api(use_port):
    set_api_resources()

    try:
        print("Endpoints available:")
        print("\tGET METHOD: http://localhost:" + use_port + '/gada_card_deck/generate?deck_offset=A&deck_size=B&randomize=C')
        print("\t\tExpecting url parameters: ", '''
            {
                "deck_offset": int (optional, default zero, >= 0),
                "deck_size": int (necessary, > 0),
                "randomize": bool (optional, default false)
            }''')
        print("================================================================")
        print("\tPOST METHOD: http://localhost:" + use_port + '/gada_card_deck/info?jsonld=A')
        print("\t\tExpecting raw json (cards) & url parameter (jsonld): ", '''
            {
                "cards": list of strings (necessary, no empty list, no empty strings),
                "jsonld": bool (optional, default false)
            }''')
        print("================================================================")

        print("\tPOST METHOD: http://localhost:" + use_port + '/high_scores')
        print("\t\tExpecting raw json: ", '''
            {
                "user_name": str (necessary, no empty string)",
                "score": int (necessary, >= 0)
            }''')
        print("\tGET METHOD: http://localhost:" + use_port + '/high_scores?page_size=A&page_offset=B')
        print("\t\tExpecting url parameters: ", '''
            {
                "page_size": int (necessary, > 0),
                "page_offset": int (optional, default zero, >= 0)
            }''')

        print("Server started")
        waitress.serve(TransLogger(app), port=use_port, threads=10)
    except:
        print("Failed to start server")
