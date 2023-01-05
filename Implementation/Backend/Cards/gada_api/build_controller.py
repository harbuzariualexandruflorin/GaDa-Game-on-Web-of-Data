import json

from flask import Flask, request
from flask_restful import Resource

from tools.api_macros import GADA_ONTOLOGY
from tools.ontology_utils import get_card_deck, cards_get_json

app = Flask(__name__)


class GADACardsBuildController(Resource):

    def __init__(self):
        pass

    def get(self):
        try:
            params = {
                "deck_offset": int(request.args.get("deck_offset", 0)),
                "deck_size": int(request.args.get("deck_size", None)),
                "randomize": request.args.get("randomize", "false").lower() == "true"
            }

            assert (params["deck_size"] > 0)
            assert (params["deck_offset"] >= 0)
            params["g"] = GADA_ONTOLOGY
        except:
            return "Invalid url parameters", 400

        cards = []
        for card_name in get_card_deck(**params):
            cards.append({
                "name": card_name,
                "score": cards_get_json(g=GADA_ONTOLOGY, cards_names=[card_name])[0]["score"]
            })
        return app.response_class(response=json.dumps({
            "cards": cards
        }), status=200, mimetype='application/json')
