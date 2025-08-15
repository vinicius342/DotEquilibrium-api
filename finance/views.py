from rest_framework import generics

from .models import Category, Debt, Expense, Income, Objective
from .serializers import (CategorySerializer, DebtSerializer,
                          ExpenseSerializer, IncomeSerializer,
                          ObjectiveSerializer)


# Objective Views
class ObjectiveListCreateView(generics.ListCreateAPIView):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer


class ObjectiveDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer
    lookup_field = 'slug'


# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class IncomeListCreateView(generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class IncomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class DebtListCreateView(generics.ListCreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer


class DebtDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
