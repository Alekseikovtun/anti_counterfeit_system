from typing import List
from flask import Flask, jsonify
from db_connector import DB_Connector

app = Flask(__name__)
connector = DB_Connector()

@app.route("/status", methods=["GET"])
def status_check():
    return jsonify({"status": "ok"})

@app.route("/insert", methods=["POST"])
def insert():
    try:
        connector.insert_data_to_test_table()
        result: List[str] = connector.get_last_data_from_test_table()
        return jsonify({"result": result})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@app.route("/all", methods=["GET"])
def get_all():
    try:
        result: List[str] = connector.get_all_data_from_test_table()
        return jsonify({"result": result})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@app.route("/last", methods=["GET"])
def get_last():
    try:
        result: List[str] = connector.get_last_data_from_test_table()
        return jsonify({"result": result})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@app.route("/delete", methods=["DELETE"])
def delete_all():
    try:
        connector.delete_all_data_from_test_table()
        return jsonify({"result": "deleted"})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)