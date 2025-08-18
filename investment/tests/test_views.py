from datetime import date

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


def test_investment_crud_and_error(api_client):
    """
    Testa as operações CRUD e cenário de erro para Investment.
    """
    # CREATE
    url = reverse('investment-list')
    data = {
        "type": "Ações",
        "amount_invested": "1000.00",
        "current_value": "1200.00",
        "date_invested": str(date(2024, 1, 1)),
        "expected_return": "15.00"
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    investment_id = response.data["id"]
    # READ
    url_detail = reverse('investment-detail', args=[investment_id])
    response = api_client.get(url_detail)
    assert response.status_code == 200
    assert response.data["type"] == "Ações"
    # UPDATE
    data_update = {
        "type": "Tesouro Direto",
        "amount_invested": "1000.00",
        "current_value": "1300.00",
        "date_invested": str(date(2024, 1, 1)),
        "expected_return": "18.00"
    }
    response = api_client.put(url_detail, data_update)
    assert response.status_code == 200
    # PARTIAL UPDATE
    response = api_client.patch(url_detail, {"current_value": "1400.00"})
    assert response.status_code == 200
    # DELETE
    response = api_client.delete(url_detail)
    assert response.status_code == 204
    # ERROR: tentar acessar investimento deletado
    response = api_client.get(url_detail)
    assert response.status_code == 404
