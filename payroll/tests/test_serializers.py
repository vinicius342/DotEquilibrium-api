from datetime import date
from decimal import Decimal

import pytest

from payroll.models import Employee
from payroll.serializers import EmployeeSerializer

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
