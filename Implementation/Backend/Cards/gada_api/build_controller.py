import json

from flask import Flask, request
from flask_restful import Resource

from tools.api_macros import GADA_ONTOLOGY
from tools.ontology_utils import get_card_deck, cards_get_json

app = Flask(__name__)


class GADACardsBuildController(Resource):

    def __init__(self):
        pass

    def post(self):
        try:
            request_json = json.loads(request.data.decode())
            params = {
                "deck_offset": request_json.get("deck_offset", 0),
                "deck_size": request_json.get("deck_size", None),
                "randomize": request_json.get("randomize", False)
            }

            assert (type(params["deck_size"]) is int and params["deck_size"] > 0)
            assert (type(params["deck_offset"]) is int and params["deck_offset"] >= 0)
            assert (type(params["randomize"]) is bool)
            params["g"] = GADA_ONTOLOGY
        except:
            return "Invalid json data", 400

        cards = []
        for card_name in get_card_deck(**params):
            cards.append({
                "name": card_name,
                "score": cards_get_json(g=GADA_ONTOLOGY, cards_names=[card_name])[0]["score"]
            })
        return app.response_class(response=json.dumps({
            "cards": cards
        }), status=200, mimetype='application/json')
