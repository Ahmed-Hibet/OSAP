from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DepositSerializer, WithdrawSerializer
from pg_python_sdk.payment_gateway_client import PaymentGatewayClient
from .models import Transaction
from access.models import User
from rest_framework.permissions import IsAuthenticated

URL = "http://167.172.141.137/"

WALLET_APP_KEY = "PG_test_d0d7faeb-06ba-4fde-bb85-c3b4b4ac62cb"

SUCCESS_URL = URL + "payment/success/"

ERROR_URL = URL + "payment/error/"

CANCEL_URL = URL + "payment/cancel/"

NOTIFY_URL = URL + "payment/notify/"

# pg = PaymentGatewayClient(key)

# transaction = pg.create_transaction(10, success_redirect_url, error_redirect_url, cancel_redirect_url, notify_url)

# transfer = pg.transfer(phone_number, amount, reason)

class Deposit(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            try:
                payment_gateway = PaymentGatewayClient(WALLET_APP_KEY)
                transaction = payment_gateway.create_transaction(
                    serializer.validated_data['amount'], 
                    SUCCESS_URL, 
                    ERROR_URL, 
                    CANCEL_URL, 
                    NOTIFY_URL
                )
                print("status code:", transaction.status)
                if transaction.status != 200:
                    return Response(str(transaction.body), status=status.HTTP_400_BAD_REQUEST)
                message = {
                    "redirect_url": transaction.body.data.checkout_url
                }
                transaction = Transaction(
                    user=request.user, 
                    amount=serializer.validated_data['amount'], 
                    payment_system="Payment gateway", 
                    _type="Deposit",
                    uuid=transaction.body.data.transaction_uuid
                )
                transaction.save()
                return Response(message, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST, template_name=None, content_type=None)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Withdraw(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = WithdrawSerializer(data=request.data)
        if serializer.is_valid():
            payment_gateway = PaymentGatewayClient(WALLET_APP_KEY)
            if request.user.balance == 0:
                return Response("You have no balance", status=status.HTTP_400_BAD_REQUEST)
            balance = request.user.balance
            if request.user.roll.roll_name == 'Respondent':
                balance = round(request.user.balance*0.95, 2)
            transfer = payment_gateway.transfer(serializer.validated_data['phone_number'], balance, "Withdraw")
            if transfer.status != 200:
                return Response(str(transfer.body), status=status.HTTP_400_BAD_REQUEST)
            print(transfer.body)
            request.user.balance = 0
            request.user.save()
            return Response("Withdraw successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Notify(APIView):
    def post(self, request, format=None):
        print(request.data)
        transaction = Transaction.objects.get(uuid=request.data['transaction_uuid'])
        transaction.status = "Completed"
        transaction.save()
        user = User.objects.get(username=transaction.user.username)
        user.balance += transaction.amount
        user.save()
        return Response(request.data, status=status.HTTP_200_OK)


class Success(APIView):
    def get(self, request, format=None):
        return HttpResponseRedirect("http://localhost:4200/researcher/dashboard/")