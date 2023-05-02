from django.shortcuts import render

# Create your views here.
#from django.contrib.auth.models import User
from .models import BankAccount
from djmoney.money import Money


from rest_framework import permissions
from .serializers import BankAccountSerializer
    

from rest_framework import generics

class balance_list(generics.ListAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        currency = self.request.query_params.get('balance_currency', None)

        queryset =  BankAccount.objects.filter(person=user,)

        if currency is not None:
            queryset = queryset.filter(balance__gt=Money(1, str(currency)))
        return queryset
    

