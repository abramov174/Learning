from django.db import models
import random
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Stock(models.Model):

    name = models.CharField(max_length=40)
    ticker = models.CharField(max_length=4, default="NULL")
    description = models.TextField(null=True, blank=True)
    currency = models.ForeignKey('Currency', null=True,  on_delete=models.SET_NULL, blank=True,)#null=True )choices=SHIRT_SIZES,
    #currency = models.CharField(max_length=1, choices=SHIRT_SIZES, default="$")
    logo = models.ImageField(null=True, blank=True)

    def get_random_price(self):
        return random.randint(0, 3000)


    def __str__(self):
        return f"{self.ticker}"


class Currency(models.Model):

    name = models.CharField(max_length=40)
    ticker = models.CharField(max_length=4)
    sign = models.CharField(max_length=1, )#choices=SHIRT_SIZES)

    def __str__(self):
        return   self.sign

# Создание доллара и рубля (символы)
Cur1 = Currency.objects.create(
    name = "Dollar",
    ticker = "1112",
    sign = "$",
)
Cur2 = Currency.objects.create(
    name = "ruble",
    ticker = "1121",
    sign = "₽",
)
Cur3 = Currency.objects.create(
        name="Euro",
        ticker="1121",
        sign="€",
    )


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class AccountCurrency(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    class Meta:
        unique_together = ['account', 'currency']

    def __str__(self):
        return f'{self.account.user.username} {self.currency.sign}'


class AccountStock(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    average_buy_cost = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=6)

    class Meta:
        unique_together = ['account', 'stock']

    def __str__(self):
        return f'{self.account.user.username} {self.stock.ticker}'
