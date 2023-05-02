from django.conf import settings
import moneyed
from djmoney.money import Money
from decimal import Decimal
import json
from rest_framework.renderers import JSONRenderer


BTC = moneyed.add_currency(
    code='BTC',
    numeric='111',
    name='bitcoin',
    countries=('NOMAD', )
)

ABA = moneyed.add_currency(
    code='ABA',
    numeric='100',
    name='aban token',
    countries=('IRAN', )
)

class CurrencyExchange:
    
    def get_rates(self, base_currency='USD'):
        
        Dict_Rate_USD = {
            "rates": {
                "BTC": 10000.0,
                "ABA": 25.0,
                "USD": 1.0,
                },
            "base": "USD",
            "date": "2023-05-01"
            }
        return Dict_Rate_USD

        
    def get_rate(self, base_currency, currency):
        return self.get_rates(base_currency).get('rates').get(currency,None)

    def validate_money(self,money):
        if not isinstance(money, Money):
            raise Exception('A Money instance must be provided')

    def get_converted_amount(self, amount, base_currency, converted_currency):
        return (Decimal(amount) / Decimal(self.get_rate(base_currency.upper(), converted_currency.upper())))

    def convert(self, money, amount, currency):
        self.validate_money(money)
        
        base_currency = str(money.currency)
        converted_currency = str(currency)
        
        if base_currency.upper() == converted_currency.upper():
            return money
        return Money(self.get_converted_amount(amount, base_currency, converted_currency), converted_currency)
