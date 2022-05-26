from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer
from .models import Message
from access.models import User


class MessageCreate(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, receiver_id):
        queryset = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver__id=receiver_id)) | 
            (Q(sender__id=receiver_id) & Q(receiver=request.user)) 
        )
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, receiver_id):
        sender = request.user
        receiver = get_object_or_404(User, pk=receiver_id)
        if ((sender.roll.roll_name != 'Admin' and receiver.roll.roll_name != 'Admin') or 
                (sender.roll.roll_name == 'Admin' and receiver.roll.roll_name == 'Admin')):
            error_message = {
                "non_field_errors": ["the chat is available only between admin and users and vice versa."]
            }
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(
            data=request.data
        )
        if serializer.is_valid():
            # print(receiver.username)
            serializer.save(sender=sender, receiver=receiver)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)