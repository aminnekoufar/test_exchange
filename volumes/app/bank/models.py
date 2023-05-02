from django.db import models
from django.contrib.auth.models import User

from djmoney.models.fields import MoneyField
from djmoney.money import Money
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator

class BankAccount(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    balance = MoneyField(
        max_digits=11,
        decimal_places=2,
        validators=[
            MinMoneyValidator({
                'USD': 1,
                'BTC': 0.00000001,
                'ABA': 1,
                }
            ),
            MaxMoneyValidator({
                'USD': 3000,
                'BTC': 3,
                'ABA': 100000,
                }
            ),
        ]
    )
    def __str__(self):
        return str(self.person)