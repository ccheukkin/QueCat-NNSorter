from flask import request, Flask, jsonify
import store.database

app = Flask(__name__)
# app.config["DEBUG"] = True

@app.route("/addRecord", methods=["POST"])
def addRecord():
    json = request.get_json()
    error = store.database.validate(json)
    if error == None:
        id = store.database.saveRecord(json)
        return {
            "status_code": 201,
            "id": id
        }
    else:
        return {
            "status_code": 400,
            "message": error
        }

@app.route("/deleteRecord", methods=["POST"])
def deleteRecord():
    id = request.args.get("id")
    error = store.database.idCheck(id)
    if error == None:
        store.database.deleteRecord(id)
        return {
            "status_code": 202
        }
    else:
        return {
            "status_code": 400,
            "message": error
        }


app.run(port=1414)