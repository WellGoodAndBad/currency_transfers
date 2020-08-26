from rest_framework import serializers
from .models import Transactions, Account, ProfileUser
# from django.contrib.auth.models import User
from rest_auth.registration.serializers import RegisterSerializer

from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class TransactionsSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(TransactionsSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['from_user'].queryset = self.fields['from_user'] \
                .queryset.filter(email=self.context['view'].request.user)

    to_user = serializers.CharField()

    class Meta:
        model = Transactions
        fields = ('to_user', 'amount')


class AccountSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('balance', 'currency')


class TransactionsViewSerialiser(serializers.ModelSerializer):

    to_user = UserSerializer()
    from_user = UserSerializer()

    class Meta:
        model = Transactions
        fields = ('amount', 'to_user', 'from_user')


class ProfileUserSerialier(serializers.ModelSerializer):

    user = UserSerializer()
    accounts = AccountSerialiser()
    transactions = TransactionsViewSerialiser(many=True, read_only=True)

    class Meta:
        model = ProfileUser
        fields = ('user', 'accounts', 'transactions')


class CurrRegistrationSerializer(RegisterSerializer):
    currency = serializers.CharField(required=True, write_only=True)
    balance = serializers.FloatField(required=True, write_only=True)

    def validate_currency(self, currency):
        if currency.lower() not in ["eur", "usd", "gpb", "rub", "btc"]:
            raise serializers.ValidationError("Currency can be only 'eur', 'usd', 'gpb', 'rub', 'btc'")
        return currency

    def validate_balance(self, balance):
        if float(balance) < 0:
            raise serializers.ValidationError("balance only > 0")
        return balance

    def get_cleaned_data(self):
        clean_data = super().get_cleaned_data()
        clean_data['currency'] = self.validated_data.get('currency', '')
        clean_data['balance'] = self.validated_data.get('balance', '')

        return clean_data

    def save(self, request):
        user = super().save(request)
        crt_account = Account.objects.create(balance=self.validated_data['balance'],
                                            currency=self.validated_data['currency'])
        crt_account.save()
        prfl = ProfileUser.objects.create(user=user, accounts=crt_account)
        prfl.save()

        return user