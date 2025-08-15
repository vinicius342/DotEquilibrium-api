from django.contrib import admin

from .models import Investment


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = (
        'type', 'amount_invested', 'current_value',
        'date_invested', 'expected_return'
    )
    list_filter = ('type', 'date_invested')
    search_fields = ('type',)
    ordering = ('-date_invested',)
