from access.serializers import RespondentSerializer, EducationLevelSerializer, OccupationSerializer
from access.models import User, EducationLevel, Occupation
from rest_framework import generics


class RespondentCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RespondentSerializer


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