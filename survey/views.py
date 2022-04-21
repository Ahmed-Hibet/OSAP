from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Survey
from .serializers import SurveySerializer
from rest_framework.permissions import IsAuthenticated


class SurveyCreate(generics.ListCreateAPIView):
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Survey.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)