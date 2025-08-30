from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from ..models import Category, Debt, Expense, Income, Objective

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


def test_create_category():
    category = Category.objects.create(
        name="Alimentação",
        description="Gastos com comida"
    )
    assert category.slug == "alimentacao"
    assert str(category) == "Alimentação"


def test_create_income(user):
    category = Category.objects.create(name="Salário")
    income = Income.objects.create(
        user=user,
        title="Recebimento",
        value=Decimal("1000.00"),
        description="Salário mensal",
        date=date.today(),
        category=category
    )
    assert str(income) == "Recebimento - 1000.00"
    assert income.category == category


def test_create_expense(user):
    category = Category.objects.create(name="Transporte")
    expense = Expense.objects.create(
        user=user,
        title="Ônibus",
        value=Decimal("4.50"),
        description="Passagem",
        date=date.today(),
        category=category
    )
    assert str(expense) == "Ônibus - 4.50"
    assert expense.category == category


def test_create_debt(user):
    category = Category.objects.create(name="Cartão")
    debt = Debt.objects.create(
        user=user,
        name="Fatura Cartão",
        value=Decimal("500.00"),
        description="Fatura do mês",
        date=date.today(),
        due_date=date.today(),
        paid=False,
        category=category
    )
    assert str(debt) == "Fatura Cartão - 500.00"
    assert not debt.paid
    assert debt.category == category


def test_update_debt(user):
    category = Category.objects.create(name="Cartão")
    debt = Debt.objects.create(
        user=user,
        name="Fatura Cartão",
        value=Decimal("500.00"),
        description="Fatura do mês",
        date=date.today(),
        due_date=date.today(),
        paid=False,
        category=category
    )
    debt.paid = True
    debt.value = Decimal("600.00")
    debt.save()
    updated = Debt.objects.get(pk=debt.pk)
    assert updated.paid is True
    assert updated.value == Decimal("600.00")


def test_delete_debt(user):
    category = Category.objects.create(name="Cartão")
    debt = Debt.objects.create(
        user=user,
        name="Fatura Cartão",
        value=Decimal("500.00"),
        description="Fatura do mês",
        date=date.today(),
        due_date=date.today(),
        paid=False,
        category=category
    )
    pk = debt.pk
    debt.delete()
    assert not Debt.objects.filter(pk=pk).exists()


def test_create_objective(user):
    objective = Objective.objects.create(
        user=user,
        title="Viagem",
        description="Viagem de férias",
        target_value=Decimal("3000.00"),
        deadline=date.today()
    )
    assert objective.slug == "viagem"
    assert str(objective) == "Viagem - 3000.00"
    assert not objective.achieved
