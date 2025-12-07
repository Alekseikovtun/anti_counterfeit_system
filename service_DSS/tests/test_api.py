import os
import sys
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from src.main import app

# upload_files endpoint tests
# # positive tests
def test_upload_one_file():
    client = app.test_client()
    
    shutil.rmtree('storage')
    os.makedirs('storage')
    
    resp = client.post("/upload_files_to_storage", data={'files': (open('example.txt', 'rb'), 'example.txt')})
    assert resp.status_code == 200

def test_upload_multiple_files():
    client = app.test_client()

    shutil.rmtree('storage')
    os.makedirs('storage')
    
    data = {
        'files': [
            (open('example.txt', 'rb'), 'example.txt'),
            (open('example2.txt', 'rb'), 'example2.txt'),
            (open('example3.txt', 'rb'), 'example3.txt')
        ]
    }

    resp = client.post("/upload_files_to_storage", data=data, content_type='multipart/form-data')
    assert resp.status_code == 200

def test_upload_different_file_types():
    client = app.test_client()
    
    shutil.rmtree('storage')
    os.makedirs('storage')

    data = {
        'files': [
            (open('example.txt', 'rb'), 'example.txt'),
            (open('example.pdf', 'rb'), 'example.pdf'),
            (open('example.png', 'rb'), 'example.png')
        ]}

    resp = client.post("/upload_files_to_storage", data=data, content_type='multipart/form-data')
    assert resp.status_code == 200

# # negative tests
def test_upload_without_file():
    client = app.test_client()
    
    shutil.rmtree('storage')
    os.makedirs('storage')
    
    resp = client.post("/upload_files_to_storage")
    assert resp.status_code == 400

def test_upload_file_with_empty_filename():
    client = app.test_client()
    
    shutil.rmtree('storage')
    os.makedirs('storage')
    
    resp = client.post("/upload_files_to_storage", data={'files': (b"content", "")})
    assert resp.status_code == 400

def test_upload_unsupported_file_type():
    client = app.test_client()
    
    shutil.rmtree('storage')
    os.makedirs('storage')
    
    resp = client.post("/upload_files_to_storage", data={'files': (open('example.gif', 'rb'), 'example.gif')})
    assert resp.status_code == 400

# get_file endpoint tests
# # positive tests
def test_get_existing_file():
    client = app.test_client()
    
    shutil.rmtree('storage')
    os.makedirs('storage')
    
    client.post("/upload_files_to_storage", data={'files': (open('example.txt', 'rb'), 'example.txt')})
    
    resp = client.get("/get_file/example.txt")
    assert resp.status_code == 200

# # negative tests
def test_get_non_existing_file():
    client = app.test_client()
    
    resp = client.get("/get_file/non_existing_file.txt")
    assert resp.status_code == 404

def test_get_file_with_no_filename():
    client = app.test_client()
    
    resp = client.get("/get_file/")
    assert resp.status_code == 404