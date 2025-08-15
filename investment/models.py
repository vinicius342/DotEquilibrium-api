from django.db import models


class Investment(models.Model):
    type = models.CharField(max_length=100)
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    current_value = models.DecimalField(max_digits=12, decimal_places=2)
    date_invested = models.DateField()
    expected_return = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.type} - {self.amount_invested}"
