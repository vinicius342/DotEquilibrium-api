from decimal import Decimal

from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Income(models.Model):
    title = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.value}"


class Expense(models.Model):
    title = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.value}"


class Debt(models.Model):
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


class Objective(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    target_value = models.DecimalField(max_digits=12, decimal_places=2)
    current_value = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    deadline = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    achieved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.target_value}"
