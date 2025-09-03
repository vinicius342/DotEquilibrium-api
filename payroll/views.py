from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (AdvancePayment, Employee, Payroll, PayrollPeriod,
                     PayrollPeriodItem)
from .serializers import (AdvancePaymentSerializer, EmployeeSerializer,
                          PayrollPeriodItemSerializer, PayrollPeriodSerializer,
                          PayrollSerializer)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PayrollPeriodViewSet(viewsets.ModelViewSet):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PayrollPeriod.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        print('DEBUG: Recebido update em PayrollPeriodViewSet', args, kwargs)
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def close_period(self, request, pk=None):
        """Fechar um período de pagamento"""
        period = self.get_object()
        if period.status == 'active':
            period.status = 'closed'
            period.save()
            return Response({'status': 'Período fechado com sucesso'})
        return Response({'error': 'Período já está fechado'}, status=400)

    @action(detail=False, methods=['get'])
    def active_period(self, request):
        """Obter o período ativo atual"""
        try:
            active_period = PayrollPeriod.objects.filter(
                user=self.request.user, status='active').first()
            if active_period:
                serializer = self.get_serializer(active_period)
                return Response(serializer.data)
            return Response({'error': 'Nenhum período ativo encontrado'},
                            status=404)
        except PayrollPeriod.DoesNotExist:
            return Response({'error': 'Nenhum período ativo encontrado'},
                            status=404)


class PayrollPeriodItemViewSet(viewsets.ModelViewSet):
    queryset = PayrollPeriodItem.objects.all()
    serializer_class = PayrollPeriodItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = PayrollPeriodItem.objects.filter(
            period__user=self.request.user)
        period_id = self.request.query_params.get('period', None)
        if period_id is not None:
            queryset = queryset.filter(period=period_id)
        return queryset


class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payroll.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdvancePaymentViewSet(viewsets.ModelViewSet):
    queryset = AdvancePayment.objects.all()
    serializer_class = AdvancePaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AdvancePayment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
