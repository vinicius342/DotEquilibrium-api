from decimal import Decimal

from django.conf import settings
from django.db import models


class PayrollPeriod(models.Model):
    """Período de folha de pagamento ativo"""
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('closed', 'Fechado'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # TODO: deve tirar o null e blank acima e tornar obrigatório
    name = models.CharField(max_length=255,
                            help_text="Nome do período")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"

    class Meta:
        ordering = ['-created_at']


class PayrollPeriodItem(models.Model):
    """Item de pagamento dentro de um período específico"""
    PAYMENT_TYPE_CHOICES = [
        ('salary', 'Salário'),
        ('daily', 'Diária'),
        ('weekly', 'Semanal'),
        ('bonus', 'Bônus'),
        ('extra', 'Hora Extra'),
        ('advance', 'Adiantamento'),
        ('other', 'Outros'),
    ]

    period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE,
                               related_name='items')
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20,
                                    choices=PAYMENT_TYPE_CHOICES,
                                    default='salary')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True,
                                    help_text="Data do pagamento (manual)")

    def __str__(self):
        type_display = dict(self.PAYMENT_TYPE_CHOICES).get(
            self.payment_type, self.payment_type)
        return f"{self.employee.name} - {type_display}: R$ {self.amount}"

    class Meta:
        ordering = ['-date_added']


class Employee(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hiring_date = models.DateField()
    termination_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Payroll(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'))
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"{self.employee.name} - {self.period_start} to " \
            f"{self.period_end}"


class AdvancePayment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_given = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    linked_payroll = models.ForeignKey(
        Payroll, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.employee.name} - {self.amount} ({self.date_given})"
