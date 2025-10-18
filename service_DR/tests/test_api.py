import os
import sys
import ast
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from main import app, connector

testing_app = app
test_connector = connector

def test_insert():
    client = testing_app.test_client()
    
    resp = client.post("/insert")
    assert resp.status_code == 200
    
    data = resp.get_json()
    assert data["result"] is not None

def test_get_last():
    client = testing_app.test_client()
    
    resp = client.get("/last")
    assert resp.status_code == 200
    
    last = resp.get_json()
    assert last["result"] is not None

def test_get_all():
    client = testing_app.test_client()
    
    resp = client.get("/all")
    assert resp.status_code == 200
    
    rows = resp.get_json().get("result", {}).get("Value", "[]")
    assert len(ast.literal_eval(rows)) >= 1

def test_delete_all():
    client = testing_app.test_client()
    
    resp = client.delete("/delete")
    assert resp.status_code == 200
    
    resp = client.get("/last")
    last = resp.get_json()
    assert last == {"result": {"Value": "[]"}}

def test_wrong_adress():
    client = testing_app.test_client()
    
    resp = client.get("/wrong_address")
    assert resp.status_code == 404
    
    resp = client.post("/wrong_address")
    assert resp.status_code == 404
    
    resp = client.delete("/wrong_address")
    assert resp.status_code == 404

def test_wrong_method():
    client = testing_app.test_client()
    
    resp = client.get("/insert")
    assert resp.status_code == 405

    resp = client.post("/last")
    assert resp.status_code == 405

    resp = client.post("/all")
    assert resp.status_code == 405

    resp = client.post("/delete")
    assert resp.status_code == 405