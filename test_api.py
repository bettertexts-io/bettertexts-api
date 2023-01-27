import json
from fastapi.testclient import TestClient

from main import app
from config import config_env

client = TestClient(app)

def test_paraphrase_ep():
    test_inputs = [{
        "input": "I am a test",
        "style": "natural",
        "medium": "text"
    }, {
        "input": "Luis ihc muss dich leider entlassen, sorry",
        "style": "formal",
        "medium": "email"
    },
    {
       "input": "Doinik bro ihc muss dich leider entlassen, sorry",
       "style": "gen-z language without being cringe bro",
       "medium": "E-Mail with greeting and ending"
    }, {
        "input": "Generate json with 3 random numbers",
        "style": "code",
        "medium": "code"
    }]


    for test_input in test_inputs:
        body = {
            "input": test_input["input"],
            "style": test_input["style"],
            "medium": test_input["medium"]
        }

        response = client.post("/api/v1/paraphrase", 
            json=body,
            headers={
                "Content-Type": "application/json", 
                "access_token": config_env["API_KEY"]
            })
        print(response.json())
        assert response.status_code == 200
        assert response.json()["results"] != []
        assert len(response.json()["results"]) == 1
