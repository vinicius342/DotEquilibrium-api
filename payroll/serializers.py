from rest_framework import serializers

from .models import (AdvancePayment, Employee, Payroll, PayrollPeriod,
                     PayrollPeriodItem)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('user',)


class PayrollPeriodItemSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name',
                                          read_only=True)
    payment_type_display = serializers.CharField(
        source='get_payment_type_display', read_only=True)

    class Meta:
        model = PayrollPeriodItem
        fields = '__all__'
        read_only_fields = ('user',)


class PayrollPeriodSerializer(serializers.ModelSerializer):
    items = PayrollPeriodItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()
    employees_count = serializers.SerializerMethodField()

    class Meta:
        model = PayrollPeriod
        fields = '__all__'
        read_only_fields = ('user',)

    def get_total_amount(self, obj):
        return sum(item.amount for item in obj.items.all())

    def get_employees_count(self, obj):
        return obj.items.values('employee').distinct().count()


class PayrollSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name',
                                          read_only=True)

    class Meta:
        model = Payroll
        fields = '__all__'
        read_only_fields = ('user',)


class AdvancePaymentSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name',
                                          read_only=True)

    class Meta:
        model = AdvancePayment
        fields = '__all__'
        read_only_fields = ('user',)
