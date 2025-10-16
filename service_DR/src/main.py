from flask import Flask, jsonify
from db_connector import DB_Connector

app = Flask(__name__)
connector = DB_Connector()

def row_to_dict(row):
    if row is None:
        return None
    try:
        return dict(row._mapping)
    except Exception:
        return {"Value": str(row)}

@app.route("/status", methods=["GET"])
def status_check():
    return jsonify({"status": "ok"})

@app.route("/insert", methods=["POST"])
def insert():
    try:
        connector.insert_data_to_test_table()
        last = connector.get_last_data_from_test_table()
        return jsonify({"result": row_to_dict(last)})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@app.route("/all", methods=["GET"])
def get_all():
    try:
        rows = connector.get_all_data_from_test_table()
        result = [row_to_dict(row) for row in rows]
        return jsonify({"result": result})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@app.route("/last", methods=["GET"])
def get_last():
    try:
        row = connector.get_last_data_from_test_table()
        return jsonify({"result": row_to_dict(row)})
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