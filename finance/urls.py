from django.urls import path

from . import views

urlpatterns = [
    # Income URLs
    path('incomes/', views.IncomeListCreateView.as_view(),
         name='income-list-create'),
    path('incomes/<int:pk>/', views.IncomeDetailView.as_view(), name='income-detail'),

    # Expense URLs
    path('expenses/', views.ExpenseListCreateView.as_view(),
         name='expense-list-create'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(),
         name='expense-detail'),

    # Debt URLs
    path('debts/', views.DebtListCreateView.as_view(), name='debt-list-create'),
    path('debts/<int:pk>/', views.DebtDetailView.as_view(), name='debt-detail'),

    # Objective URLs
    path('objectives/', views.ObjectiveListCreateView.as_view(),
         name='objective-list-create'),
    path('objectives/<int:pk>/', views.ObjectiveDetailView.as_view(),
         name='objective-detail'),

    # Category URLs
    path('categories/', views.CategoryListCreateView.as_view(),
         name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(),
         name='category-detail'),
]
