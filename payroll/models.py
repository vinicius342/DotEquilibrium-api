from decimal import Decimal

from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hiring_date = models.DateField()
    termination_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'))
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"{self.employee.name} - {self.period_start} to {self.period_end}"


class AdvancePayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_given = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    linked_payroll = models.ForeignKey(
        Payroll, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.employee.name} - {self.amount} ({self.date_given})"
