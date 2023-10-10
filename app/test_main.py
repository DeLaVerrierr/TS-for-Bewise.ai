from fastapi.testclient import TestClient

from main import app


client = TestClient(app)

def test_generation_num():
    response = client.post("/generation-num/", json={"questions_num": 5})
    assert response.status_code == 200

def test_get_random_question():
    response = client.get("/get-random-question/")
    assert response.status_code == 200

# def test_submit_answer():
#     response = client.post("/submit-answer/?q=13", json={"answer":"Canal Zone"})
#     assert response.status_code == 200