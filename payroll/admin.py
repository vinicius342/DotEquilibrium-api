from django.contrib import admin

from .models import Employee, PayrollPeriod, PayrollPeriodItem


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'salary',
                    'hiring_date', 'termination_date')
    search_fields = ('name', 'role')
    list_filter = ('role', 'hiring_date', 'termination_date')


@admin.register(PayrollPeriodItem)
class PayrollPeriodItemAdmin(admin.ModelAdmin):
    list_display = ('employee', 'payment_type', 'amount', 'is_processed',
                    'date_added')
    search_fields = ('employee__name', 'description')
    list_filter = ('payment_type', 'is_processed', 'date_added')


@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'status', 'user')
    search_fields = ('name',)
    list_filter = ('status',)
