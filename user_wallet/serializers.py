from rest_framework import serializers
from user_wallet.models import WalletDetails
#  PayAmount, Transactions


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = WalletDetails
        fields = ['id', 'balance', 'user_upi']
        extra_kwargs = {'balance': {'read_only': True},
                        'user_upi': {'read_only': True}}
