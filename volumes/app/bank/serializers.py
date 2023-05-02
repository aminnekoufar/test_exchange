from rest_framework import serializers
from djmoney.contrib.django_rest_framework import MoneyField

from .models import BankAccount



class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('balance_currency','balance')