# type: ignore
from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from finance.models import Category, Objective
from finance.serializers import (CategorySerializer, DebtSerializer,
                                 ExpenseSerializer, IncomeSerializer,
                                 ObjectiveSerializer)

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


def test_category_serializer_create():
    """
    Deve criar uma categoria e gerar o slug automaticamente.
    """
    data = {"name": "Educação", "description": "Cursos e livros"}
    serializer = CategorySerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.name == "Educação"
    assert instance.slug == "educacao"


def test_category_serializer_to_representation():
    """
    Deve serializar uma categoria existente corretamente.
    """
    category = Category.objects.create(name="Saúde", description="Remédios")
    serializer = CategorySerializer(category)
    data = serializer.data
    assert data["name"] == "Saúde"
    assert "slug" in data


def test_income_serializer_create(user):
    category = Category.objects.create(name="Salário")
    data = {
        "title": "Recebimento",
        "value": "1000.00",
        "description": "Salário mensal",
        "date": str(date.today()),
        "category": category.pk
    }
    serializer = IncomeSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    income = serializer.save(user=user)
    assert income.title == "Recebimento"
    assert income.value == Decimal("1000.00")


def test_expense_serializer_create(user):
    category = Category.objects.create(name="Transporte")
    data = {
        "title": "Ônibus",
        "value": "4.50",
        "description": "Passagem",
        "date": str(date.today()),
        "category": category.pk
    }
    serializer = ExpenseSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    expense = serializer.save(user=user)
    assert expense.title == "Ônibus"
    assert expense.value == Decimal("4.50")


def test_debt_serializer_create(user):
    category = Category.objects.create(name="Cartão")
    data = {
        "name": "Fatura Cartão",
        "value": "500.00",
        "description": "Fatura do mês",
        "date": str(date.today()),
        "due_date": str(date.today()),
        "paid": False,
        "category": category.pk
    }
    serializer = DebtSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    debt = serializer.save(user=user)
    assert debt.name == "Fatura Cartão"
    assert debt.value == Decimal("500.00")
    assert not debt.paid


def test_objective_serializer_create(user):
    data = {
        "title": "Viagem",
        "description": "Viagem de férias",
        "target_value": "3000.00",
        "deadline": str(date.today())
    }
    serializer = ObjectiveSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    obj = serializer.save(user=user)
    assert obj.title == "Viagem"
    assert obj.target_value == Decimal("3000.00")


def test_objective_serializer_to_representation(user):
    obj = Objective.objects.create(
        user=user,
        title="Casa",
        description="Comprar casa",
        target_value="100000.00",
        deadline=date.today()
    )
    serializer = ObjectiveSerializer(obj)
    data = serializer.data
    assert data["title"] == "Casa"
    assert "slug" in data
