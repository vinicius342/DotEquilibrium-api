from rest_framework import generics

from .models import AdvancePayment, Employee, Payroll
from .serializers import (AdvancePaymentSerializer, EmployeeSerializer,
                          PayrollSerializer)


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class PayrollListCreateView(generics.ListCreateAPIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer


class PayrollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer


class AdvancePaymentListCreateView(generics.ListCreateAPIView):
    queryset = AdvancePayment.objects.all()
    serializer_class = AdvancePaymentSerializer


class AdvancePaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdvancePayment.objects.all()
    serializer_class = AdvancePaymentSerializer
