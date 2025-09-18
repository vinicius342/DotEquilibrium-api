from rest_framework import serializers

from .models import (Category, Debt, Expense, Income, Objective,
                     ObjectiveDeposit, RecurringBill, RecurringBillPayment)


class ObjectiveDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectiveDeposit
        fields = '__all__'
        read_only_fields = ('objective',)


class ObjectiveSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()
    remaining_amount = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    category_display = serializers.CharField(source='get_category_display',
                                             read_only=True)
    deposits = ObjectiveDepositSerializer(many=True, read_only=True)

    class Meta:
        model = Objective
        fields = '__all__'
        read_only_fields = ('user', 'achieved', 'completed_at')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'
        read_only_fields = ('user',)


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ('user',)


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = '__all__'
        read_only_fields = ('user',)


class RecurringBillPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringBillPayment
        fields = '__all__'


class RecurringBillSerializer(serializers.ModelSerializer):
    # Incluir informações de pagamento para um período específico
    payment_for_period = serializers.SerializerMethodField()

    class Meta:
        model = RecurringBill
        fields = '__all__'
        read_only_fields = ('user',)

    def get_payment_for_period(self, obj):
        """
        Retorna informações de pagamento para o período especificado na query
        """
        request = self.context.get('request')
        if request:
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            if year and month:
                payment = obj.get_payment_for_period(int(year), int(month))
                if payment:
                    return RecurringBillPaymentSerializer(payment).data
        return None
