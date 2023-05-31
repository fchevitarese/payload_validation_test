import pytest
from marshmallow import ValidationError

from schemas.apolice_schema import Payload1Schema, Payload2Schema
from pytest_mock import mocker

from app import app, handle_payload
from tasks import validate_car_payload, validate_house_payload


@pytest.fixture
def client():
    return app.test_client()


def test_handle_payload_with_valid_house_payload(client, mocker):
    mock_queues = mocker.patch("app.queues")
    mock_q = mock_queues.get.return_value
    mock_job = mock_q.enqueue.return_value

    payload = {
        "produto": 111,
        "item": {
            "endereço": {"rua": "rua x", "numero": 123},
            "inquilino": {"nome": "jose", "CPF": 12345678912},
            "beneficiario": {"nome": "Imobiliaria X", "CNPJ": 12345678912345},
        },
        "valores": {"precoTotal": 1200.00, "parcelas": 6},
    }
    response = client.post("/payload", json=payload)

    assert response.status_code == 200
    assert "Payload enqueued successfully" in response.json["message"]

    mock_queues.get.assert_called_once_with("house")
    assert "Job id" in response.json["message"]


def test_handle_payload_with_valid_car_payload(client, mocker):
    mock_queues = mocker.patch("app.queues")
    mock_q = mock_queues.get.return_value
    mock_job = mock_q.enqueue.return_value
    payload = {
        "produto": 111,
        "item": {"placa": "ABC1234", "chassis": 123213, "modelo": "PORCHE"},
        "valores": {"precoTotal": 3000.00, "parcelas": 12},
    }
    response = client.post("/payload", json=payload)

    assert response.status_code == 200
    assert "Payload enqueued successfully" in response.json["message"]


def test_handle_payload_with_invalid_payload(client):
    payload = {}
    response = client.post("/payload", json=payload)

    assert response.status_code == 400
    assert "error" in response.json


def test_handle_payload_with_exception(client):
    payload = {
        "item": {"endereço": "Rua de teste"},
    }
    response = client.post("/payload", json=payload)

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json == {
        "error": {"valores": ["valores é um campo obrigatório"]}
    }


def test_handle_car_payload_missing_information(client):
    payload = {
        "produto": 111,
        "item": {"placa": "ABC1234", "chassis": 123213},
        "valores": {"precoTotal": 3000.00, "parcelas": 12},
    }
    response = client.post("/payload", json=payload)

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json == {
        "error": {"item": {"modelo": ["Missing data for required field."]}}
    }
