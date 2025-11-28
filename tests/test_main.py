import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app 

client = TestClient(app)

@patch("main.fetch_products_from_odoo")
def test_read_dashboard(mock_fetch):
    mock_fetch.return_value = [
        {"id": 1, "name": "Test Chair", "standard_price": 50.0, "default_code": "TEST_001"}
    ]

    response = client.get("/")

    assert response.status_code == 200
    assert "Test Chair" in response.text
    assert "50.00" in response.text

@patch("main.update_product_cost_in_odoo")
def test_update_cost_success(mock_update):
    mock_update.return_value = True

    payload = {"product_id": 1, "new_cost": 100.0}
    response = client.post("/update_cost", json=payload)

    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_update_cost_negative_value():
    payload = {"product_id": 1, "new_cost": -50.0}
    response = client.post("/update_cost", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Cost cannot be negative!"

def test_update_cost_invalid_type():
    payload = {"product_id": 1, "new_cost": "hilal"}
    response = client.post("/update_cost", json=payload)

    assert response.status_code == 422
