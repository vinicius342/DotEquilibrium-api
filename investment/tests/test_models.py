from datetime import date
from decimal import Decimal

import pytest

from investment.models import Investment

pytestmark = pytest.mark.django_db


def test_investment_crud():
    # CREATE
    investment = Investment.objects.create(
        type="Ações",
        amount_invested=Decimal("1000.00"),
        current_value=Decimal("1200.00"),
        date_invested=date(2024, 1, 1),
        expected_return=Decimal("15.00")
    )
    assert investment.pk is not None
    # READ
    fetched = Investment.objects.get(pk=investment.pk)
    assert fetched.type == "Ações"
    assert fetched.amount_invested == Decimal("1000.00")
    assert fetched.current_value == Decimal("1200.00")
    assert fetched.date_invested == date(2024, 1, 1)
    assert fetched.expected_return == Decimal("15.00")
    # UPDATE
    fetched.type = "Tesouro Direto"
    fetched.save()
    updated = Investment.objects.get(pk=investment.pk)
    assert updated.type == "Tesouro Direto"
    # __str__
    assert str(updated) == "Tesouro Direto - 1000.00"
    # DELETE
    updated.delete()
    assert not Investment.objects.filter(pk=investment.pk).exists()
    # CREATE sem expected_return
    inv2 = Investment.objects.create(
        type="CDB",
        amount_invested=Decimal("2000.00"),
        current_value=Decimal("2100.00"),
        date_invested=date(2024, 3, 10)
    )
    assert inv2.expected_return is None
