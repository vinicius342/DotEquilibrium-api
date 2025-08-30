from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import Category

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    user = get_user_model().objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client

# CATEGORY


def test_category_crud_and_error(api_client):
    """
    Testa CRUD básico e cenário de erro para Category.
    """
    # Create
    url = reverse('category-list')
    data = {
        "name": "Alimentação",
        "description": "Gastos com comida"
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    slug = response.data["slug"]
    # Retrieve
    url_detail = reverse('category-detail', args=[slug])
    response = api_client.get(url_detail)
    assert response.status_code == 200
    assert response.data["name"] == "Alimentação"
    # Update
    data_update = {
        "name": "Alimentação Atualizada",
        "description": "Nova descrição"
    }
    response = api_client.put(url_detail, data_update)
    assert response.status_code == 200
    # Partial update
    response = api_client.patch(
        url_detail, {"description": "Só descrição alterada"}
    )
    assert response.status_code == 200
    # Delete
    response = api_client.delete(url_detail)
    assert response.status_code == 204
    # Error: retrieve inexistente
    response = api_client.get(url_detail)
    assert response.status_code == 404

# INCOME


def test_income_crud_and_error(api_client):
    """
    Testa CRUD básico e cenário de erro para Income.
    """
    category = Category.objects.create(name="Salário")
    # Create
    url = reverse('income-list')
    data = {
        "title": "Recebimento",
        "value": "1000.00",
        "description": "Salário mensal",
        "date": str(date.today()),
        "category": category.pk
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    income_id = response.data["id"]
    # Retrieve
    url_detail = reverse('income-detail', args=[income_id])
    response = api_client.get(url_detail)
    assert response.status_code == 200
    assert response.data["title"] == "Recebimento"
    # Update
    data_update = {
        "title": "Recebimento Atualizado",
        "value": "2000.00",
        "description": "Novo salário",
        "date": str(date.today()),
        "category": category.pk
    }
    response = api_client.put(url_detail, data_update)
    assert response.status_code == 200
    # Partial update
    response = api_client.patch(
        url_detail, {"description": "Só descrição alterada"}
    )
    assert response.status_code == 200
    # Delete
    response = api_client.delete(url_detail)
    assert response.status_code == 204
    # Error: retrieve inexistente
    response = api_client.get(url_detail)
    assert response.status_code == 404

# EXPENSE


def test_expense_crud_and_error(api_client):
    """
    Testa CRUD básico e cenário de erro para Expense.
    """
    category = Category.objects.create(name="Transporte")
    # Create
    url = reverse('expense-list')
    data = {
        "title": "Ônibus",
        "value": "4.50",
        "description": "Passagem",
        "date": str(date.today()),
        "category": category.pk
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    expense_id = response.data["id"]
    # Retrieve
    url_detail = reverse('expense-detail', args=[expense_id])
    response = api_client.get(url_detail)
    assert response.status_code == 200
    assert response.data["title"] == "Ônibus"
    # Update
    data_update = {
        "title": "Uber",
        "value": "20.00",
        "description": "Corrida de Uber",
        "date": str(date.today()),
        "category": category.pk
    }
    response = api_client.put(url_detail, data_update)
    assert response.status_code == 200
    # Partial update
    response = api_client.patch(
        url_detail, {"description": "Só descrição alterada"}
    )
    assert response.status_code == 200
    # Delete
    response = api_client.delete(url_detail)
    assert response.status_code == 204
    # Error: retrieve inexistente
    response = api_client.get(url_detail)
    assert response.status_code == 404

# DEBT


def test_debt_crud_and_error(api_client):
    """
    Testa CRUD básico e cenário de erro para Debt.
    """
    category = Category.objects.create(name="Cartão")
    # Create
    url = reverse('debt-list')
    data = {
        "name": "Fatura Cartão",
        "value": "500.00",
        "description": "Fatura do mês",
        "date": str(date.today()),
        "due_date": str(date.today()),
        "paid": False,
        "category": category.pk
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    debt_id = response.data["id"]
    # Retrieve
    url_detail = reverse('debt-detail', args=[debt_id])
    response = api_client.get(url_detail)
    assert response.status_code == 200
    assert response.data["name"] == "Fatura Cartão"
    # Update
    data_update = {
        "name": "Fatura Cartão Atualizada",
        "value": "600.00",
        "description": "Nova descrição",
        "date": str(date.today()),
        "due_date": str(date.today()),
        "paid": True,
        "category": category.pk
    }
    response = api_client.put(url_detail, data_update)
    assert response.status_code == 200
    # Partial update
    response = api_client.patch(url_detail, {"paid": True})
    assert response.status_code == 200
    # Delete
    response = api_client.delete(url_detail)
    assert response.status_code == 204
    # Error: retrieve inexistente
    response = api_client.get(url_detail)
    assert response.status_code == 404

# OBJECTIVE


def test_objective_crud_and_error(api_client):
    """Testa CRUD básico e cenário de erro para Objective."""
    # Create
    url = reverse('objective-list')
    data = {
        "title": "Viagem",
        "description": "Viagem de férias",
        "target_value": "3000.00",
        "deadline": str(date.today())
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    slug = response.data["slug"]
    # Retrieve
    url_detail = reverse('objective-detail', args=[slug])
    response = api_client.get(url_detail)
    assert response.status_code == 200
    assert response.data["title"] == "Viagem"
    # Update
    data_update = {
        "title": "Viagem Atualizada",
        "description": "Nova descrição",
        "target_value": "4000.00",
        "deadline": str(date.today()),
        "achieved": True
    }
    response = api_client.put(url_detail, data_update)
    assert response.status_code == 200
    # Partial update
    response = api_client.patch(url_detail, {"achieved": True})
    assert response.status_code == 200
    # Delete
    response = api_client.delete(url_detail)
    assert response.status_code == 204
    # Error: retrieve inexistente
    response = api_client.get(url_detail)
    assert response.status_code == 404
