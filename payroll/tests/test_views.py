from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from payroll.models import Employee

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    user = get_user_model().objects.create_user(
        username='testuser', password='testpass')
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def test_employee_crud_and_error(api_client):
    """
    Testa CRUD e erro para Employee.
    """
    url = reverse('employee-list')
    data = {
        "name": "Maria Souza",
        "role": "Analista",
        "salary": "4000.00",
        "hiring_date": str(date(2023, 1, 5))
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    emp_id = response.data["id"]
    url_detail = reverse('employee-detail', args=[emp_id])
    response = api_client.get(url_detail)
    assert response.status_code == 200
    # Update
    response = api_client.put(url_detail, {**data, "role": "Coordenadora"})
    assert response.status_code == 200
    # Partial update
    response = api_client.patch(url_detail, {"salary": "4500.00"})
    assert response.status_code == 200
    # Delete
    response = api_client.delete(url_detail)
    assert response.status_code == 204
    # Error
    response = api_client.get(url_detail)
    assert response.status_code == 404
