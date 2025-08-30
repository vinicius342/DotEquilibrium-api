from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Income(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.value}"


class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.value}"


class Debt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.value}"


class RecurringBillPayment(models.Model):
    """
    Modelo para registrar o pagamento de uma conta recorrente 
    em um período específico.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('paid', 'Pago'),
        ('overdue', 'Atrasado'),
    ]

    recurring_bill = models.ForeignKey(
        'RecurringBill',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    # Período do pagamento (ano e mês)
    year = models.IntegerField()
    month = models.IntegerField()  # 1-12

    # Status específico para este período
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Data do pagamento (quando foi marcado como pago)
    paid_date = models.DateTimeField(null=True, blank=True)

    # Valor pago (pode ser diferente do valor padrão da conta)
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Observações sobre este pagamento específico
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Garante que não haverá duplicatas para a mesma conta no mesmo período
        unique_together = ('recurring_bill', 'year', 'month')
        verbose_name = "Pagamento de Conta Recorrente"
        verbose_name_plural = "Pagamentos de Contas Recorrentes"
        indexes = [
            models.Index(fields=['year', 'month']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        status_display = dict(self.STATUS_CHOICES).get(
            self.status, self.status)
        return f"{self.recurring_bill.name} - {self.month:02d}/{self.year} - {status_display}"

    @property
    def due_date(self):
        """Calcula a data de vencimento para este período específico."""
        from datetime import date
        try:
            return date(self.year, self.month, self.recurring_bill.due_day)
        except ValueError:
            # Para casos onde o dia não existe no mês (ex: 31 de fevereiro)
            from calendar import monthrange
            last_day = monthrange(self.year, self.month)[1]
            due_day = min(self.recurring_bill.due_day, last_day)
            return date(self.year, self.month, due_day)

    @property
    def is_overdue(self):
        """Verifica se o pagamento está atrasado."""
        from datetime import date
        return self.status == 'pending' and date.today() > self.due_date

    def mark_as_paid(self, amount=None, notes=''):
        """Marca o pagamento como pago."""
        from django.utils import timezone
        self.status = 'paid'
        self.paid_date = timezone.now()
        if amount:
            self.amount_paid = amount
        if notes:
            self.notes = notes
        self.save()

    def mark_as_pending(self):
        """Marca o pagamento como pendente."""
        self.status = 'pending'
        self.paid_date = None
        self.amount_paid = None
        self.save()


class RecurringBill(models.Model):
    FREQUENCY_CHOICES = [
        ('monthly', 'Mensal'),
        ('weekly', 'Semanal'),
        ('yearly', 'Anual'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    due_day = models.IntegerField(help_text="Dia do vencimento (1-31)")
    frequency = models.CharField(
        max_length=10, choices=FREQUENCY_CHOICES, default='monthly')
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    deactivated_at = models.DateTimeField(
        null=True, blank=True, help_text="Data em que a conta foi desativada"
    )

    class Meta:
        verbose_name = "Conta Recorrente"
        verbose_name_plural = "Contas Recorrentes"

    def __str__(self):
        return f"{self.name} - R$ {self.value} (dia {self.due_day})"

    def get_payment_for_period(self, year, month):
        """
        Retorna o pagamento para um período específico.
        Se não existir, retorna None.
        """
        try:
            return self.payments.get(year=year, month=month)
        except RecurringBillPayment.DoesNotExist:
            return None

    def get_or_create_payment_for_period(self, year, month):
        """
        Retorna ou cria um pagamento para um período específico.
        """
        payment, created = self.payments.get_or_create(
            year=year,
            month=month,
            defaults={'status': 'pending'}
        )
        return payment, created

    def get_status_for_period(self, year, month):
        """
        Retorna o status para um período específico.
        Se não houver registro, retorna 'pending'.
        """
        payment = self.get_payment_for_period(year, month)
        return payment.status if payment else 'pending'

    def mark_paid_for_period(self, year, month, amount=None, notes=''):
        """
        Marca como pago para um período específico.
        """
        payment, created = self.get_or_create_payment_for_period(year, month)
        payment.mark_as_paid(amount or self.value, notes)
        return payment

    def mark_pending_for_period(self, year, month):
        """
        Marca como pendente para um período específico.
        """
        payment = self.get_payment_for_period(year, month)
        if payment:
            payment.mark_as_pending()
        return payment

    def deactivate(self):
        """
        Desativa a conta recorrente a partir da data atual.
        """
        from django.utils import timezone
        self.deactivated_at = timezone.now()
        self.is_active = False
        self.save()

    def is_active_for_period(self, year, month):
        """
        Verifica se a conta estava ativa no período especificado.
        """
        if not self.deactivated_at:
            return self.is_active

        # Calcular o primeiro dia do período
        from datetime import date
        period_start = date(year, month, 1)

        # Se foi desativada antes do período, não deve aparecer
        return self.deactivated_at.date() > period_start


class Objective(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    target_value = models.DecimalField(max_digits=12, decimal_places=2)
    current_value = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    deadline = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    achieved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.target_value}"
