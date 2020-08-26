from .serializers import ProfileUserSerialier, TransactionsSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from .service import make_transfer
from .models import ProfileUser


class ProfileViewSet(viewsets.ModelViewSet):

    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileUserSerialier

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProfileUser.objects.all()
        else:
            return ProfileUser.objects.filter(user__id=self.request.user.id)


class TransferViewSet(viewsets.ModelViewSet):

    authentication_classes = (BasicAuthentication,)
    serializer_class = TransactionsSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        from_account = ProfileUser.objects.get(user__id=self.request.user.id)
        to_account = ProfileUser.objects.get(user__email=self.request.data['to_user'])

        transaction = make_transfer(from_account, to_account, float(self.request.data['amount']))
        from_account.transactions.add(transaction)
        to_account.transactions.add(transaction)

        return Response(serializer.data, status=status.HTTP_201_CREATED)