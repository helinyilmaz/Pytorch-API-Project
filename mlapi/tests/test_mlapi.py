import pytest
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from src.main import app


@pytest.fixture
def client():
    FastAPICache.init(InMemoryBackend())
    with TestClient(app) as c:
        yield c
        
# Project tests

def test_predict(client):
    data = {"text": ["I hate you.", "I love you."]}
    response = client.post(
        "/project/bulk-predict",
        json=data,
    )
    print(response.json())
    assert response.status_code == 200
    assert isinstance(response.json()["predictions"], list)
    assert isinstance(response.json()["predictions"][0], list)
    assert isinstance(response.json()["predictions"][0][0], dict)
    assert isinstance(response.json()["predictions"][1][0], dict)
    assert set(response.json()["predictions"][0][0].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][0][1].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][1][0].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][1][1].keys()) == {"label", "score"}
    assert response.json()["predictions"][0][0]["label"] == "NEGATIVE"
    assert response.json()["predictions"][0][1]["label"] == "POSITIVE"
    assert response.json()["predictions"][1][0]["label"] == "POSITIVE"
    assert response.json()["predictions"][1][1]["label"] == "NEGATIVE"

def test_predict_empty_text(client):
    data = {"text": []}
    response = client.post("/project/bulk-predict", json=data)
    assert response.status_code == 200
    assert response.json()["predictions"] == []

def test_predict_single_text(client):
    data = {"text": ["I love coding."]}
    response = client.post("/project/bulk-predict", json=data)
    assert response.status_code == 200
    assert isinstance(response.json()["predictions"][0], list)

def test_predict_invalid_type(client):
    data = {"text": [123, None, True]}
    response = client.post("/project/bulk-predict", json=data)
    assert response.status_code == 422

def test_predict_score_range(client):
    data = {"text": ["I hate this.", "I love this."]}
    response = client.post("/project/bulk-predict", json=data)
    for predictions in response.json()["predictions"]:
        for pred in predictions:
            assert 0.0 <= pred["score"] <= 1.0

def test_predict_wrong_method(client):
    response = client.get("/project/bulk-predict")
    assert response.status_code == 405

def test_predict_missing_key(client):
    data = {"texts": ["I love this."]}
    response = client.post("/project/bulk-predict", json=data)
    assert response.status_code == 422


# Lap API tests

def test_health(client):
    response = client.get("/lab/health")
    assert response.status_code == 200
    assert "time" in response.json()
    assert "T" in response.json()["time"]


def test_health_post_not_allowed(client):
    response = client.post("/lab/health")
    assert response.status_code == 405


def test_hello_valid(client):
    response = client.get("/lab/hello?name=Helin")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Helin"}


def test_hello_numeric_name(client):
    name = "12345"
    response = client.get(f"/lab/hello?name={name}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Hello {name}"


def test_hello_special_characters(client):
    name = "Hélin_123!@"
    response = client.get(f"/lab/hello?name={name}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Hello {name}"


def test_hello_url_encoded_spaces(client):
    response = client.get("/lab/hello?name=Helin%20Yilmaz")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello Helin Yilmaz"


def test_hello_long_name(client):
    long_name = "a" * 1000
    response = client.get(f"/lab/hello?name={long_name}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Hello ")


def test_hello_extra_query_params(client):
    response = client.get("/lab/hello?name=Helin&age=25&city=Berkeley")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello Helin"


def test_hello_missing_name(client):
    response = client.get("/lab/hello")
    assert response.status_code == 422


def test_hello_empty_name(client):
    response = client.get("/lab/hello?name=")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello "


# ------------------------------
# Lab /predict endpoint tests
# ------------------------------
def test_predict_basic(client):
    data = {
        "MedInc": 1, "HouseAge": 1, "AveRooms": 3, "AveBedrms": 3,
        "Population": 3, "AveOccup": 5, "Latitude": 1, "Longitude": 1
    }
    response = client.post("/lab/predict", json=data)
    assert response.status_code == 200
    assert isinstance(response.json()["prediction"], float)


def test_predict_invalid_latitude(client):
    bad = {
        "MedInc": 1, "HouseAge": 1, "AveRooms": 3, "AveBedrms": 3,
        "Population": 3, "AveOccup": 5, "Latitude": 123, "Longitude": -118
    }
    response = client.post("/lab/predict", json=bad)
    assert response.status_code == 422


def test_predict_invalid_longitude(client):
    bad = {
        "MedInc": 1, "HouseAge": 1, "AveRooms": 3, "AveBedrms": 3,
        "Population": 3, "AveOccup": 5, "Latitude": 34, "Longitude": -200
    }
    response = client.post("/lab/predict", json=bad)
    assert response.status_code == 422


def test_predict_missing_field(client):
    bad = {
        "MedInc": 1, "HouseAge": 1,
        "AveBedrms": 3, "Population": 3, "AveOccup": 5,
        "Latitude": 34, "Longitude": -118
    }
    response = client.post("/lab/predict", json=bad)
    assert response.status_code == 422


def test_predict_wrong_type(client):
    bad = {
        "MedInc": "not_a_number", "HouseAge": 1, "AveRooms": 3, "AveBedrms": 3,
        "Population": 3, "AveOccup": 5, "Latitude": 34, "Longitude": -118
    }
    response = client.post("/lab/predict", json=bad)
    assert response.status_code == 422


def test_predict_extra_field(client):
    bad = {
        "MedInc": 1, "HouseAge": 1, "AveRooms": 3, "AveBedrms": 3,
        "Population": 3, "AveOccup": 5, "Latitude": 34, "Longitude": -118,
        "ExtraField": "should_not_be_here"
    }
    response = client.post("/lab/predict", json=bad)
    assert response.status_code == 422


def test_predict_latitude_boundaries(client):
    valid_min = {
        "MedInc": 1, "HouseAge": 1, "AveRooms": 3, "AveBedrms": 3,
        "Population": 3, "AveOccup": 5, "Latitude": -90, "Longitude": 0
    }
    valid_max = {
        "MedInc": 1, "HouseAge": 1, "AveRooms": 3, "AveBedrms": 3,
        "Population": 3, "AveOccup": 5, "Latitude": 90, "Longitude": 0
    }
    response_min = client.post("/lab/predict", json=valid_min)
    response_max = client.post("/lab/predict", json=valid_max)
    assert response_min.status_code == 200
    assert response_max.status_code == 200


def test_predict_longitude_boundaries(client):
    valid_min = {
        "MedInc": 1, "HouseAge": 1, "AveRooms": 3, "AveBedrms": 3,
        "Population": 3, "AveOccup": 5, "Latitude": 0, "Longitude": -180
    }
    valid_max = {
        "MedInc": 1, "HouseAge": 1, "AveRooms": 3, "AveBedrms": 3,
        "Population": 3, "AveOccup": 5, "Latitude": 0, "Longitude": 180
    }
    response_min = client.post("/lab/predict", json=valid_min)
    response_max = client.post("/lab/predict", json=valid_max)
    assert response_min.status_code == 200
    assert response_max.status_code == 200


# ------------------------------
# Lab /bulk-predict tests
# ------------------------------
def test_bulk_predict_basic(client):
    data = {
        "houses": [
            {"MedInc": 1, "HouseAge": 1, "AveRooms": 3, "AveBedrms": 3,
             "Population": 3, "AveOccup": 5, "Latitude": 1, "Longitude": 1},
            {"MedInc": 0, "HouseAge": 1, "AveRooms": 3, "AveBedrms": 3,
             "Population": 3, "AveOccup": 5, "Latitude": 1, "Longitude": 1},
        ]
    }
    response = client.post("/lab/bulk-predict", json=data)
    assert response.status_code == 200
    assert len(response.json()["predictions"]) == 2


def test_bulk_predict_single_house(client):
    data = {
        "houses": [
            {"MedInc": 1, "HouseAge": 1, "AveRooms": 3, "AveBedrms": 3,
             "Population": 3, "AveOccup": 5, "Latitude": 1, "Longitude": 1},
        ]
    }
    response = client.post("/lab/bulk-predict", json=data)
    assert response.status_code == 200
    assert len(response.json()["predictions"]) == 1


def test_bulk_predict_empty_list(client):
    data = {"houses": []}
    response = client.post("/lab/bulk-predict", json=data)
    assert response.status_code == 200
    assert response.json()["predictions"] == []


def test_root_not_found(client):
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}