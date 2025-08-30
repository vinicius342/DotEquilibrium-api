from django.contrib import admin

from .models import Category, Debt, Expense, Income, Objective, RecurringBill


@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_value',
                    'current_value', 'deadline', 'achieved')
    search_fields = ('title', 'description')
    list_filter = ('achieved', 'deadline', 'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'date', 'category')
    search_fields = ('title', 'description', 'category')
    list_filter = ('date', 'category')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'date', 'category')
    search_fields = ('title', 'description', 'category')
    list_filter = ('date', 'category')


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'date', 'due_date', 'paid')
    search_fields = ('name', 'description')
    list_filter = ('date', 'due_date', 'paid')


@admin.register(RecurringBill)
class RecurringBillAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'due_day', 'frequency', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('frequency', 'category', 'is_active', 'created_at')
    ordering = ('due_day', 'name')


admin.site.site_header = "Finance Admin"
admin.site.site_title = "Finance Admin Portal"
admin.site.index_title = "Welcome to the Finance Admin Portal"
