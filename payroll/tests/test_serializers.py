from datetime import date
from decimal import Decimal

import pytest

from payroll.models import Employee
from payroll.serializers import (AdvancePaymentSerializer, EmployeeSerializer,
                                 PayrollSerializer)

pytestmark = pytest.mark.django_db


def test_employee_serializer_create():
    """
    Deve criar um funcionário válido.
    """
    data = {
        "name": "Lucas Alves",
        "role": "QA",
        "salary": "3500.00",
        "hiring_date": str(date(2023, 2, 1))
    }
    serializer = EmployeeSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    emp = serializer.save()
    assert emp.name == "Lucas Alves"
    assert emp.salary == Decimal("3500.00")


def test_payroll_serializer_create():
    """
    Deve criar uma folha de pagamento válida.
    """
    emp = Employee.objects.create(
        name="Julia Lima",
        role="RH",
        salary=Decimal("4000.00"),
        hiring_date=date(2022, 5, 10)
    )
    data = {
        "employee": emp.pk,
        "period_start": str(date(2023, 7, 1)),
        "period_end": str(date(2023, 7, 31)),
        "gross_amount": "4000.00",
        "deductions": "200.00",
        "net_amount": "3800.00",
        "payment_date": str(date(2023, 8, 5))
    }
    serializer = PayrollSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    payroll = serializer.save()
    assert payroll.gross_amount == Decimal("4000.00")
    assert payroll.net_amount == Decimal("3800.00")


def test_advancepayment_serializer_create():
    """
    Deve criar um adiantamento válido.
    """
    emp = Employee.objects.create(
        name="Paulo Souza",
        role="Financeiro",
        salary=Decimal("4200.00"),
        hiring_date=date(2021, 5, 10)
    )
    data = {
        "employee": emp.pk,
        "date_given": str(date(2023, 7, 15)),
        "amount": "900.00",
        "description": "Adiantamento de férias"
    }
    serializer = AdvancePaymentSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    adv = serializer.save()
    assert adv.amount == Decimal("900.00")
