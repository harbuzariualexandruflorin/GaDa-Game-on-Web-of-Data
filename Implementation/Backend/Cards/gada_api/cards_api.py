import waitress
from flask_restful import Api
from paste.translogger import TransLogger

from gada_api.build_controller import *
from gada_api.high_scores_controller import GADAHighScoresController
from gada_api.info_controller import GADACardsInfoController


def set_api_resources():
    api = Api(app)
    api.add_resource(GADACardsBuildController, '/gada_card_deck/build')
    api.add_resource(GADACardsInfoController, '/gada_card_deck/info')
    api.add_resource(GADAHighScoresController, '/high_scores')


def start_api(use_port):
    set_api_resources()

    try:
        print("Endpoints available:")
        print("\tPOST METHOD: http://localhost:" + use_port + '/gada_card_deck/build')
        print("\t\tExpecting raw json: ", '''
            {
                "deck_offset": int (optional, default zero, >= 0),
                "deck_size": int (necessary, > 0),
                "randomize": bool (optional, default false)
            }''')
        print("================================================================")
        print("\tPOST METHOD: http://localhost:" + use_port + '/gada_card_deck/info')
        print("\t\tExpecting raw json: ", '''
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
