from flask import request, Flask, jsonify
from store.database import Database
import store.validation as validation
import inference.inference as inference


app = Flask(__name__)
# app.config["DEBUG"] = True
database = Database()


@app.route("/add", methods=["POST"])
def addRecord():
    json = request.get_json()
    error = validation.validateRecord(json, database)

    if error != None:
        return {
            "status_code": 400,
            "message": error
        }

    id = database.createRecord(json["text"], json["categories"])
    return {
        "status_code": 201,
        "id": id
    }
        

@app.route("/delete", methods=["POST"])
def deleteRecord():
    id = request.args.get("id")
    error = database.recordExist(id)

    if error != None:
        return {
            "status_code": 400,
            "message": error
        }

    database.deleteRecord(id)
    return {
        "status_code": 202
    }


@app.route("/infer", methods=["GET"])
def infer():
    json = request.get_json()
    error = validation.validateText(json)

    if error != None:
        return {
            "status_code": 400,
            "message": error
        }

    categories = inference.run(json["text"])
    return {
        "status_code": 200,
        "categories": categories
    }


app.run(port=1414)