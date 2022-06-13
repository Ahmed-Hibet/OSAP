from rest_framework import serializers

class DepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=0)


class WithdrawSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)