from django.contrib.auth.models import User
from user_wallet.models import WalletDetails
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user_upi = user.username + '@' + str(user.id)
        wallet_details = WalletDetails(
            user=user, user_upi=user_upi, balance=0)
        wallet_details.save()
        return user
