import json

from flask import Flask, request
from flask_restful import Resource

from tools.api_macros import GADA_ONTOLOGY
from tools.ontology_utils import cards_get_json, cards_get_json_ld

app = Flask(__name__)


class GADACardsInfoController(Resource):

    def __init__(self):
        pass

    def post(self):
        try:
            request_json = json.loads(request.data.decode())
            jsonld = request_json.get("jsonld", False)
            params = {"cards_names": request_json.get("cards", None)}

            assert (type(jsonld) is bool)
            assert (type(params["cards_names"]) is list and len(params["cards_names"]) > 0)
            for card in params["cards_names"]:
                assert (type(card) is str and len(card) > 0)
            params["g"] = GADA_ONTOLOGY
        except:
            return "Invalid json data", 400

        return app.response_class(response=json.dumps({
            "cards": cards_get_json(**params) if not jsonld else cards_get_json_ld(**params)
        }), status=200, mimetype='application/json')
