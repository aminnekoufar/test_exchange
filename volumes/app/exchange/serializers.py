from rest_framework import serializers
from djmoney.contrib.django_rest_framework import MoneyField

class RateSerializer(serializers.Serializer):
    rates = serializers.DictField()
    base = serializers.CharField(max_length=20)
    date = serializers.CharField(max_length=20)


class checkSerializer(serializers.Serializer):
    balance_currency = serializers.CharField()
    balance_amount = MoneyField(max_digits=12, decimal_places=4)
    converted_currency = serializers.CharField()
    converted_amount = MoneyField(max_digits=12, decimal_places=4)

class ConfirmCheckSerializer(serializers.Serializer):
    balance_currency = serializers.CharField()
    balance_amount = MoneyField(max_digits=12, decimal_places=4)
    converted_currency = serializers.CharField()
    confirm_converted = serializers.CharField()
