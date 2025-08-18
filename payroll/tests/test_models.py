from datetime import date
from decimal import Decimal

import pytest

from payroll.models import AdvancePayment, Employee, Payroll

pytestmark = pytest.mark.django_db


def test_payroll_models_crud():
    # Employee
    emp = Employee.objects.create(
        name="João Silva",
        role="Desenvolvedor",
        salary=Decimal("5000.00"),
        hiring_date=date(2022, 1, 10)
    )
    assert emp.name == "João Silva"
    assert str(emp) == "João Silva"
    # Payroll
    payroll = Payroll.objects.create(
        employee=emp,
        period_start=date(2023, 7, 1),
        period_end=date(2023, 7, 31),
        gross_amount=Decimal("5000.00"),
        deductions=Decimal("500.00"),
        net_amount=Decimal("4500.00"),
        payment_date=date(2023, 8, 5)
    )
    assert payroll.gross_amount == Decimal("5000.00")
    assert payroll.net_amount == Decimal("4500.00")
    assert str(payroll) == "João Silva - 2023-07-01 to 2023-07-31"
    # AdvancePayment
    advance = AdvancePayment.objects.create(
        employee=emp,
        date_given=date(2023, 7, 15),
        amount=Decimal("1000.00"),
        description="Adiantamento de férias",
        linked_payroll=payroll
    )
    assert advance.amount == Decimal("1000.00")
    assert advance.linked_payroll == payroll
    assert str(advance) == "João Silva - 1000.00 (2023-07-15)"
    # UPDATE
    emp.role = "Tech Lead"
    emp.save()
    assert Employee.objects.get(pk=emp.pk).role == "Tech Lead"
    # DELETE
    advance.delete()
    assert not AdvancePayment.objects.filter(pk=advance.pk).exists()
    payroll.delete()
    assert not Payroll.objects.filter(pk=payroll.pk).exists()
    emp.delete()
    assert not Employee.objects.filter(pk=emp.pk).exists()
