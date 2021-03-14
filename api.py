from flask import request, Flask, jsonify
from store.database import Database
import store.validation as validation
import yaml
from pathlib import Path
import nn.inference


app = Flask(__name__)
# app.config["DEBUG"] = True
database = Database()
model = None
path = Path(__file__).parent / "./inference-config.yml"
with open(path) as file:
    yml = yaml.load(file, Loader=yaml.FullLoader)
    assert "modelPath" in yml.keys(), 'The key "modelPath" is not defined in the inference-config.yml file'
    modelPath = yml["modelPath"]
    model = nn.inference.Categorizer(modelPath)


@app.route("/add", methods=["POST"])
def addRecords():
    json = request.get_json()
    error = validation.validateRecords(json, database)

    if error != None:
        return {
            "status_code": 400,
            "message": error
        }

    id = database.recordsCreate(json["records"])
    return {
        "status_code": 201,
        "id": id
    }
        

@app.route("/delete", methods=["POST"])
def deleteRecord():
    json = request.get_json()
    error = validation.validateRecordIds(json, database)

    if error != None:
        return {
            "status_code": 400,
            "message": error
        }

    database.recordsDelete(json["ids"])
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

    categories = model.run(json["text"])
    return {
        "status_code": 200,
        "categories": categories
    }


app.run(port=1414)