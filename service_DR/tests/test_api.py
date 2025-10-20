import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from main import app

def test_insert():
    client = app.test_client()
    
    resp = client.post("/insert")
    assert resp.status_code == 200
    
    data = resp.get_json()
    assert data["result"] is not None

def test_get_last():
    client = app.test_client()
    
    resp = client.get("/last")
    assert resp.status_code == 200
    
    last = resp.get_json()
    assert last["result"] is not None

def test_get_all_empty_list():
    client = app.test_client()
    
    resp = client.delete("/delete")
    assert resp.status_code == 200

    resp = client.get("/all")
    assert resp.status_code == 200
    
    list_of_data = resp.get_json().get("result", {})
    assert len(list_of_data) == 0 

def test_get_all_not_empty_list():
    client = app.test_client()
    
    resp = client.post("/insert")
    assert resp.status_code == 200

    resp = client.get("/all")
    assert resp.status_code == 200
    
    list_of_data = resp.get_json().get("result", {})
    assert len(list_of_data) >= 1

def test_delete_all():
    client = app.test_client()
    
    resp = client.post("/insert")
    assert resp.status_code == 200

    resp = client.delete("/delete")
    assert resp.status_code == 200
    
    resp = client.get("/last")
    last = resp.get_json()
    assert last == {"result": []}

def test_wrong_adress():
    client = app.test_client()
    
    resp = client.get("/wrong_address")
    assert resp.status_code == 404
    
    resp = client.post("/wrong_address")
    assert resp.status_code == 404
    
    resp = client.delete("/wrong_address")
    assert resp.status_code == 404

def test_wrong_method():
    client = app.test_client()
    
    resp = client.get("/insert")
    assert resp.status_code == 405

    resp = client.post("/last")
    assert resp.status_code == 405

    resp = client.post("/all")
    assert resp.status_code == 405

    resp = client.post("/delete")
    assert resp.status_code == 405