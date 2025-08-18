from datetime import date
from decimal import Decimal

import pytest

from investment.models import Investment
from investment.serializers import InvestmentSerializer

pytestmark = pytest.mark.django_db


def test_investment_serializer_create():
    """
    Deve criar um investimento válido a partir dos dados do serializer.
    """
    data = {
        "type": "Ações",
        "amount_invested": "1000.00",
        "current_value": "1200.00",
        "date_invested": str(date(2024, 1, 1)),
        "expected_return": "15.00"
    }
    serializer = InvestmentSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    investment = serializer.save()
    assert investment.type == "Ações"
    assert investment.amount_invested == Decimal("1000.00")
    assert investment.expected_return == Decimal("15.00")


def test_investment_serializer_to_representation():
    """
    Deve serializar um investimento existente corretamente.
    """
    investment = Investment.objects.create(
        type="CDB",
        amount_invested=Decimal("2000.00"),
        current_value=Decimal("2100.00"),
        date_invested=date(2024, 3, 10)
    )
    serializer = InvestmentSerializer(investment)
    data = serializer.data
    assert data["type"] == "CDB"
    assert data["amount_invested"] == "2000.00"
    assert data["expected_return"] is None
