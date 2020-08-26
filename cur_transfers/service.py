from .models import Transactions
from django.db import transaction


def currency_converter(value, in_curr, out_curr) -> float:
    cur_dict = {
                'RUB': 1,
                'BTC': 867745,
                'USD': 73.6376,
                'EUR': 87.1722,
                'GBP': 96.4211
    }
    return (cur_dict[in_curr] / cur_dict[out_curr]) * value


def make_transfer(from_user, to_user, amount):

    from_cur = from_user.accounts.currency.upper()
    to_cur = to_user.accounts.currency.upper()

    if from_user.accounts.balance < amount:
        raise(ValueError('Not enough money'))
    if from_user == to_user:
        raise(ValueError('Chose another user'))

    with transaction.atomic():
        from_balance = from_user.accounts.balance - amount
        from_user.accounts.balance = from_balance
        from_user.accounts.save()

        if from_cur != to_cur:
            amount = currency_converter(value=amount, in_curr=from_cur, out_curr=to_cur)

        to_balance = to_user.accounts.balance + amount
        to_user.accounts.balance = to_balance
        to_user.accounts.save()

        transfer = Transactions.objects.create(
            from_user=from_user.user,
            to_user=to_user.user,
            amount=amount
        )

    return transfer


