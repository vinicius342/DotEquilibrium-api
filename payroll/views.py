from rest_framework import viewsets

from .models import AdvancePayment, Employee, Payroll
from .serializers import (AdvancePaymentSerializer, EmployeeSerializer,
                          PayrollSerializer)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer


class AdvancePaymentViewSet(viewsets.ModelViewSet):
    queryset = AdvancePayment.objects.all()
    serializer_class = AdvancePaymentSerializer
