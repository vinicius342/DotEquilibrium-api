from django.contrib import admin

from .models import (AdvancePayment, Employee, Payroll, PayrollPeriod,
                     PayrollPeriodItem)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'salary',
                    'hiring_date', 'termination_date')
    search_fields = ('name', 'role')
    list_filter = ('role', 'hiring_date', 'termination_date')


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'period_start', 'period_end', 'gross_amount',
                    'net_amount', 'payment_date')
    search_fields = ('employee__name',)
    list_filter = ('payment_date', 'period_start', 'period_end')


@admin.register(AdvancePayment)
class AdvancePaymentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'amount', 'date_given', 'linked_payroll')
    search_fields = ('employee__name', 'description')
    list_filter = ('date_given',)


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
