from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from rest_framework import generics

from rest_framework.response import Response
from rest_framework import authentication, permissions

from bank.currencies import CurrencyExchange
from bank.models import BankAccount
from bank.serializers import BankAccountSerializer

from exchange.serializers import RateSerializer,checkSerializer,ConfirmCheckSerializer
from djmoney.money import Money
from decimal import Decimal

class ExchangeView(APIView):

    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        check = CurrencyExchange()
        return Response(check.get_rates())

class ConvertCheckView(generics.ListAPIView):

    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self,):
        user = self.request.user
        currency = self.request.query_params.get('balance_currency', 'USD')

        queryset =  BankAccount.objects.filter(person=user,balance__gt=Money(1, str(currency)))

        return queryset

    
    def get(self,request):
        que = self.get_queryset()
        wallet = que.get().balance
        data = CurrencyExchange()

        convert_currency = request.query_params.get('convert_currency', 'USD')

        res = { 
            "balance_currency" : wallet.currency,
            "balance_amount" : wallet.amount,
            "converted_currency": convert_currency,
            "converted_amount": data.convert(wallet,wallet.amount,convert_currency),
        }
        respond = checkSerializer(res)
        return Response(respond.data,status=200)

class ConfirmConvertView(generics.GenericAPIView):
    serializer_class = ConfirmCheckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self,Dcurrency=None):
        user = self.request.user

        if not Dcurrency:
            currency = self.request.query_params.get('balance_currency', 'USD')
        else:
            currency = Dcurrency

        queryset =  BankAccount.objects.filter(person=user,balance__gt=Money(1, str(currency)))

        return queryset

    
    def get(self,request):
        que = self.get_queryset()
        wallet = que.get().balance
        data = CurrencyExchange()
        
        convert_currency = request.query_params.get('convert_currency', 'USD')

        self.res = {
            "balance_currency" : wallet.currency,
            "balance_amount" : wallet.amount,
            "converted_currency": convert_currency,
            "converted_amount": data.convert(wallet,Decimal(1),convert_currency),
        }
        respond = checkSerializer(self.res)
        return Response(respond.data,status=200)
    
    def post(self, request, *args, **kwargs):
        que = self.get_queryset()

        data = CurrencyExchange()

        C_balance_currency = request.POST["balance_currency"]
        C_balance_amount = request.POST["balance_amount"]
        C_converted_currency = request.POST["converted_currency"]
        confirm_text = request.POST["confirm_converted"]

        wallet = que.get()


        converted_amount = data.convert(wallet.balance,C_balance_amount,C_converted_currency)
        # from IPython import embed;embed();exit()

        if C_balance_currency == str(wallet.balance.currency) and \
            Decimal(C_balance_amount) <= wallet.balance.amount and \
            C_converted_currency in data.get_rates().get('rates') and \
            confirm_text == '1234':
                wallet.balance.amount = wallet.balance.amount - Decimal(C_balance_amount)
                wallet.save()


                old_wallet = self.get_queryset(Dcurrency=C_converted_currency)
                if old_wallet:
                    changes_wallet = old_wallet.get()
                    changes_wallet.balance.amount += converted_amount.amount
                    changes_wallet.save()
                else:
                    new_wallet = BankAccount.objects.create(person=request.user,balance=converted_amount)
                    new_wallet.save()

                return Response('Yes',status=200)
        return Response('m',status=200)
        