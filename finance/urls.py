from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('objectives', views.ObjectiveViewSet)
router.register('incomes', views.IncomeViewSet)
router.register('expenses', views.ExpenseViewSet)
router.register('debts', views.DebtViewSet)
router.register('recurring-bills', views.RecurringBillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
