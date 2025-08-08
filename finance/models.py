from django.db import models


class Income(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.description} - {self.value}"


class Expense(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.description} - {self.value}"


class Debt(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    due_date = models.DateField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description} - {self.value}"
