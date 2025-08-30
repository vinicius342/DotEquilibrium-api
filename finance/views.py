from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (Category, Debt, Expense, Income, Objective, RecurringBill,
                     RecurringBillPayment)
from .serializers import (CategorySerializer, DebtSerializer,
                          ExpenseSerializer, IncomeSerializer,
                          ObjectiveSerializer, RecurringBillPaymentSerializer,
                          RecurringBillSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


class ObjectiveViewSet(viewsets.ModelViewSet):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Objective.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Debt.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecurringBillViewSet(viewsets.ModelViewSet):
    queryset = RecurringBill.objects.all()
    serializer_class = RecurringBillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecurringBill.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """
        Marca uma conta recorrente como paga para um período específico
        """
        bill = self.get_object()
        year = request.data.get('year')
        month = request.data.get('month')
        amount = request.data.get('amount')
        notes = request.data.get('notes', '')

        if not year or not month:
            return Response(
                {'error': 'Year and month are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payment = bill.mark_paid_for_period(
                int(year), int(month), amount, notes
            )
            serializer = RecurringBillPaymentSerializer(payment)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def mark_pending(self, request, pk=None):
        """
        Marca uma conta recorrente como pendente para um período específico
        """
        bill = self.get_object()
        year = request.data.get('year')
        month = request.data.get('month')

        if not year or not month:
            return Response(
                {'error': 'Year and month are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payment = bill.mark_pending_for_period(int(year), int(month))
            if payment:
                serializer = RecurringBillPaymentSerializer(payment)
                return Response(serializer.data)
            else:
                return Response(
                    {'message': 'No payment record found for this period'},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Desativa uma conta recorrente a partir da data atual
        """
        bill = self.get_object()
        try:
            bill.deactivate()
            serializer = self.get_serializer(bill)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
