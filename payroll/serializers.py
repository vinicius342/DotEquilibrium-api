from rest_framework import serializers

from .models import AdvancePayment, Employee, Payroll


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = '__all__'


class AdvancePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvancePayment
        fields = '__all__'
