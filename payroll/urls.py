from django.urls import path

from . import views

urlpatterns = [
    # Employee URLs
    path('employees/', views.EmployeeListCreateView.as_view(),
         name='employee-list-create'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(),
         name='employee-detail'),

    # Payroll URLs
    path('payrolls/', views.PayrollListCreateView.as_view(),
         name='payroll-list-create'),
    path('payrolls/<int:pk>/', views.PayrollDetailView.as_view(),
         name='payroll-detail'),

    # AdvancePayment URLs
    path('advance-payments/', views.AdvancePaymentListCreateView.as_view(),
         name='advance-payment-list-create'),
    path('advance-payments/<int:pk>/', views.AdvancePaymentDetailView.as_view(),
         name='advance-payment-detail'),
]
