from datetime import date
from decimal import Decimal

import pytest

from payroll.models import Employee

pytestmark = pytest.mark.django_db


def test_employee_model_crud():
    # Employee
    emp = Employee.objects.create(
        name="João Silva",
        role="Desenvolvedor",
        salary=Decimal("5000.00"),
        hiring_date=date(2022, 1, 10)
    )
    assert emp.name == "João Silva"
    assert str(emp) == "João Silva"

    # UPDATE
    emp.role = "Tech Lead"
    emp.save()
    assert Employee.objects.get(pk=emp.pk).role == "Tech Lead"

    # DELETE
    emp.delete()
    assert not Employee.objects.filter(pk=emp.pk).exists()
