import json
import sqlite3

from flask import Flask, request
from flask_restful import Resource

from tools.sqlite_utils import insert_high_score, read_table_high_scores

app = Flask(__name__)


class GADAHighScoresController(Resource):

    def __init__(self):
        pass

    def get(self):
        try:
            params = {
                "page_offset": int(request.args.get("page_offset", 0)),
                "page_size": int(request.args.get("page_size", None))
            }

            assert (params["page_offset"] >= 0)
            assert (params["page_size"] > 0)
        except:
            return "Invalid url parameters", 400

        return app.response_class(response=json.dumps({
            "scores": read_table_high_scores(**params)
        }), status=200, mimetype='application/json')

    def post(self):
        try:
            request_json = json.loads(request.data.decode())
            params = {
                "user_name": request_json.get("user_name", None),
                "score": request_json.get("score", None),
            }

            assert (type(params["score"]) is int and params["score"] >= 0)
            assert (type(params["user_name"]) is str and len(params["user_name"]) > 0)
        except:
            return "Invalid json data", 400

        try:
            insert_high_score(**params)
        except sqlite3.IntegrityError:
            return "Username already exists or score is not a valid number", 400
        return "High score added", 200
