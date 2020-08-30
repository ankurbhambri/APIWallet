from datetime import datetime
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from user_wallet.models import (WalletDetails, Transactions)
from user_wallet.serializers import WalletSerializer


def try_or(fn, default, *args, **kwargs):
    """
    Usage: try_or(lambda: request_user.email, None, *args, **kwargs)
    """
    try:
        return fn(*args, **kwargs)
    except Exception:
        return default


class WalletDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to see wallet details.
    """
    queryset = WalletDetails.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class AddAmountViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to be Add Amount.
    Post request = {
        "amount": ""
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, pk=None):
        wallet = WalletDetails.objects.get(user__id=request.user.id)
        tranx_history = {
            "sender": "self",
            "receiver": "self",
            "transaction_type": "credited",
            "credited_amount": request.data.get("amount"),
            "balance": wallet.balance,
        }
        Transactions.objects.create(wallet=wallet, extra_feild=tranx_history)
        wallet.balance += request.data.get("amount")
        wallet.save()

        data = {"user_upi": wallet.user_upi, "balance": wallet.balance,
                "amount": request.data.get("amount"),
                "status": "Amount Added To Your Wallet Sucessfully"}
        return Response(data)


class PayAmountViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to be Pay Amount.
    Post request = {
        "user_upi": "",
        "pay_amount": ""
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, pk=None):
        user_upi = try_or(lambda: request.data.get("user_upi"), '')
        pay_amount = try_or(lambda: request.data.get("pay_amount"), 0)
        receiver_wallet = WalletDetails.objects.filter(user_upi=user_upi)
        sender_wallet = WalletDetails.objects.get(user=request.user)
        sender_context = {}

        if receiver_wallet:
            if sender_wallet.balance >= pay_amount:
                receiver_wallet[0].balance += pay_amount
                sender_wallet.balance = sender_wallet.balance - pay_amount
                sender_wallet.save()
                receiver_wallet[0].save()
                sender_context = {
                    "sender": sender_wallet.user_upi,
                    "receiver": user_upi,
                    "transaction_type": "debited",
                    "deducted_amount": pay_amount,
                    "balance_left": sender_wallet.balance,
                }
                Transactions.objects.create(
                    wallet=sender_wallet, extra_feild=sender_context)

                receiver_context = {
                    "sender": sender_wallet.user_upi,
                    "receiver": "self",
                    "transaction_type": "credited",
                    "credited_amount": pay_amount,
                    "balance": receiver_wallet[0].balance,
                }
                Transactions.objects.create(
                    wallet=receiver_wallet[0], extra_feild=receiver_context)
                return Response(sender_context)
            else:
                sender_context = {"status": "Check your balance is low!"}

        return Response(sender_context)


class TransactionsViewSet(viewsets.ViewSet):
    """
    API endpoint that prints a user month wise transactions.
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_upi = request.user.walletdetails_set.values_list(
            'user_upi', flat=True)[0]
        today = datetime.today()
        credited_amount = 0
        deducted_amount = 0
        wallet_balance = 0
        data = {
            "user_upi": user_upi,
            "user_name": request.user.username,
            "current_month_credited_amount": credited_amount,
            "current_month_deducted_amount": deducted_amount,
            "wallet_balance": wallet_balance
        }
        queryset = Transactions.objects.filter(wallet__user_upi=user_upi)
        if queryset:
            wallet_balance = queryset[0].wallet.balance
            for value in queryset:
                if value.created_at.month == today.month:
                    if value.extra_feild['transaction_type'] == 'credited':
                        credited_amount += value.extra_feild['credited_amount']
                    else:
                        deducted_amount = value.extra_feild['deducted_amount']

        data.update({
            "current_month_credited_amount": credited_amount,
            "current_month_deducted_amount": deducted_amount,
            "wallet_balance": wallet_balance
        })

        return Response(data)
