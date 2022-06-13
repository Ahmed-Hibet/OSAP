from access.serializers import (
    RespondentSerializer, 
    EducationLevelSerializer, 
    OccupationSerializer,
    UserCreateSerializer,
)
from access.models import User, EducationLevel, Occupation
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Roll


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        roll, created = Roll.objects.get_or_create(roll_name='Researcher')
        serializer.save(roll=roll)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = User.objects.get(pk=request.user.id)
        if not user.roll or user.roll.roll_name != 'Respondent':
            serializer = UserCreateSerializer(user)
        else:
            serializer = RespondentSerializer(user)
        return Response(serializer.data)

    # def get_queryset(self):
    #     return User.objects.filter(id=self.request.user.id)
    
    # def get_serializer_class(self):
    #     if self.request.user.roll.roll_name == 'Respondent':
    #         return RespondentSerializer
    #     return UserCreateSerializer


class RespondentCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RespondentSerializer

    def perform_create(self, serializer):
        roll, created = Roll.objects.get_or_create(roll_name='Respondent')
        serializer.save(roll=roll)


class EducationLevelCreate(generics.ListCreateAPIView):
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer


class EducationLevelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer


class OccupationCreate(generics.ListCreateAPIView):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer


class OccupationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer