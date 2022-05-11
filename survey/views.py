from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Survey, RespondentHistory
from .serializers import SurveySerializer, SurveyFillSerializer
from .permissions import IsRespondent
import datetime
from django.db.models import Q


class SurveyCreate(generics.ListCreateAPIView):
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.roll.roll_name == 'Researcher':
            return Survey.objects.filter(owner=self.request.user)
        
        age = None
        if self.request.user.birth_date:
            age = (datetime.date.today() - self.request.user.birth_date).days
            age//=365
    
        survey = Survey.objects.filter(
                is_active=True,
                expired_date__gte=datetime.date.today()
            ).filter(
                Q(requirements__gender="Both") | 
                Q(requirements__gender=self.request.user.gender)
            ).filter(
                Q(requirements__occupations__isnull=True) |
                Q(requirements__occupations__id=self.request.user.occupation.id)
            ).filter(
                Q(requirements__education_levels__isnull=True) |
                Q(requirements__education_levels__id=self.request.user.education_level.id)
            ).filter(
                ~Q(pk__in=[history.survey.id for history in RespondentHistory.objects.filter(respondent=self.request.user)])
            )

        if not age:
            survey = survey.filter(
                requirements__minimum_age__isnull=True, 
                requirements__maximum_age__isnull=True
            )
        else:
            survey = survey.filter(
                Q(requirements__minimum_age__isnull=True) | 
                Q(requirements__minimum_age__lte=age)
            ).filter(
                Q(requirements__maximum_age__isnull=True) | 
                Q(requirements__maximum_age__gte=age)
            )
        return survey
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SurveyFill(APIView):
    permission_classes = [IsAuthenticated, IsRespondent]

    def post(self, request, format=None):
        serializer = SurveyFillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(respondent=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)