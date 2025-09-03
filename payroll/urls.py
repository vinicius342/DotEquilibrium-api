from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('employees', views.EmployeeViewSet)
router.register('payroll-periods', views.PayrollPeriodViewSet)
router.register('payroll-period-items', views.PayrollPeriodItemViewSet)
router.register('payrolls', views.PayrollViewSet)
router.register('advance-payments', views.AdvancePaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
