from datetime import date, datetime
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from ..models import Category, RecurringBill

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def category():
    return Category.objects.create(
        name="Utilidades",
        description="Contas básicas"
    )


@pytest.fixture
def recurring_bill(user, category):
    return RecurringBill.objects.create(
        user=user,
        name="Conta de Luz",
        description="Conta mensal de energia",
        value=Decimal("150.00"),
        due_day=15,
        frequency='monthly',
        category=category
    )


def test_create_recurring_bill(recurring_bill):
    """Testa a criação de uma conta recorrente"""
    assert str(recurring_bill) == "Conta de Luz - R$ 150.00 (dia 15)"
    assert recurring_bill.is_active
    assert recurring_bill.deactivated_at is None


def test_recurring_bill_payment_for_period(recurring_bill):
    """Testa o sistema de pagamentos por período"""
    year, month = 2024, 8

    # Inicialmente não deve ter pagamento para este período
    payment = recurring_bill.get_payment_for_period(year, month)
    assert payment is None

    # Criar pagamento para o período
    payment, created = recurring_bill.get_or_create_payment_for_period(
        year, month
    )
    assert created
    assert payment.status == 'pending'
    assert payment.year == year
    assert payment.month == month

    # Verificar se não cria duplicata
    payment2, created2 = recurring_bill.get_or_create_payment_for_period(
        year, month
    )
    assert not created2
    assert payment.id == payment2.id


def test_mark_bill_as_paid_for_period(recurring_bill):
    """Testa marcar conta como paga para um período específico"""
    year, month = 2024, 8
    amount = Decimal("145.00")
    notes = "Pago com desconto"

    payment = recurring_bill.mark_paid_for_period(year, month, amount, notes)

    assert payment.status == 'paid'
    assert payment.amount_paid == amount
    assert payment.notes == notes
    assert payment.paid_date is not None


def test_mark_bill_as_pending_for_period(recurring_bill):
    """Testa marcar conta como pendente para um período específico"""
    year, month = 2024, 8

    # Primeiro marca como pago
    payment = recurring_bill.mark_paid_for_period(year, month)
    assert payment.status == 'paid'

    # Depois marca como pendente
    payment = recurring_bill.mark_pending_for_period(year, month)
    assert payment.status == 'pending'
    assert payment.paid_date is None
    assert payment.amount_paid is None


def test_get_status_for_period(recurring_bill):
    """Testa obter status para um período específico"""
    year, month = 2024, 8

    # Sem pagamento registrado, deve retornar 'pending'
    status = recurring_bill.get_status_for_period(year, month)
    assert status == 'pending'

    # Criar e marcar como pago
    recurring_bill.mark_paid_for_period(year, month)
    status = recurring_bill.get_status_for_period(year, month)
    assert status == 'paid'


def test_soft_delete_recurring_bill(recurring_bill):
    """Testa o soft delete (desativação) de uma conta recorrente"""
    # Conta deve estar ativa inicialmente
    assert recurring_bill.is_active
    assert recurring_bill.deactivated_at is None

    # Desativar a conta
    recurring_bill.deactivate()

    # Verificar se foi desativada corretamente
    assert not recurring_bill.is_active
    assert recurring_bill.deactivated_at is not None
    assert isinstance(recurring_bill.deactivated_at, datetime)


def test_is_active_for_period(recurring_bill):
    """Testa se a conta estava ativa em um período específico"""
    # Conta criada em agosto de 2024
    current_date = timezone.now()

    # Deve estar ativa para períodos atuais
    assert recurring_bill.is_active_for_period(
        current_date.year, current_date.month
    )

    # Desativar a conta
    recurring_bill.deactivate()

    # Não deve estar ativa para períodos futuros após desativação
    future_month = (
        current_date.month + 1 if current_date.month < 12 else 1
    )
    future_year = (
        current_date.year if current_date.month < 12
        else current_date.year + 1
    )

    assert not recurring_bill.is_active_for_period(future_year, future_month)

    # Mas deve estar ativa para períodos anteriores à desativação
    past_month = (
        current_date.month - 1 if current_date.month > 1 else 12
    )
    past_year = (
        current_date.year if current_date.month > 1
        else current_date.year - 1
    )

    assert recurring_bill.is_active_for_period(past_year, past_month)


def test_recurring_bill_payment_due_date(recurring_bill):
    """Testa o cálculo da data de vencimento para um pagamento"""
    year, month = 2024, 8

    payment, _ = recurring_bill.get_or_create_payment_for_period(year, month)

    expected_due_date = date(2024, 8, 15)  # due_day = 15
    assert payment.due_date == expected_due_date


def test_recurring_bill_payment_due_date_invalid_day(user, category):
    """Testa o cálculo da data de vencimento para dias inválidos no mês"""
    # Conta com vencimento no dia 31
    bill = RecurringBill.objects.create(
        user=user,
        name="Conta Teste",
        value=Decimal("100.00"),
        due_day=31,
        frequency='monthly',
        category=category
    )

    # Fevereiro não tem dia 31
    payment, _ = bill.get_or_create_payment_for_period(2024, 2)

    # Deve usar o último dia do mês (29 em 2024 por ser ano bissexto)
    expected_due_date = date(2024, 2, 29)
    assert payment.due_date == expected_due_date


def test_recurring_bill_payment_is_overdue(recurring_bill):
    """Testa a verificação de pagamentos atrasados"""
    # Criar pagamento para um mês passado
    past_year = 2024
    past_month = 1  # Janeiro

    payment, _ = recurring_bill.get_or_create_payment_for_period(
        past_year, past_month
    )

    # Como está pendente e a data já passou, deve estar atrasado
    # Nota: Este teste pode falhar dependendo da data atual
    # Para um teste mais robusto, seria melhor mockar a data atual
    if date.today() > payment.due_date:
        assert payment.is_overdue


def test_recurring_bill_payment_str_representation(recurring_bill):
    """Testa a representação string do pagamento"""
    year, month = 2024, 8

    payment, _ = recurring_bill.get_or_create_payment_for_period(year, month)

    expected_str = "Conta de Luz - 08/2024 - Pendente"
    assert str(payment) == expected_str

    # Marcar como pago e testar novamente
    payment.mark_as_paid()
    expected_str_paid = "Conta de Luz - 08/2024 - Pago"
    assert str(payment) == expected_str_paid
