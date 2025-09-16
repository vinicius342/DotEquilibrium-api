from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('employees', views.EmployeeViewSet)
router.register('payroll-periods', views.PayrollPeriodViewSet)
router.register('payroll-period-items', views.PayrollPeriodItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
