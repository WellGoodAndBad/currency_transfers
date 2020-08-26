from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()


class Account(models.Model):
    balance = models.FloatField(validators=[MinValueValidator(0)], blank=True)
    currency = models.CharField(max_length=16)


class Transactions(models.Model):
    amount = models.FloatField(validators=[MinValueValidator(0)])
    from_user = models.ForeignKey(User,
                                  on_delete=models.PROTECT,
                                  related_name='from_user')
    to_user = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                related_name='to_user')


class ProfileUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accounts = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    transactions = models.ManyToManyField(Transactions, related_name='transactions', blank=True)