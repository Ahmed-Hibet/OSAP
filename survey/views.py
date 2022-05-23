from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Survey, RespondentHistory, QuestionnaireType
from .serializers import (
    SurveySerializer, 
    SurveyFillSerializer, 
    QuestionnaireTypeSerializer,
    SurveyAnalyseSerializer,
    ChoiceResponseSerializer
)
from .permissions import IsRespondent, IsAdminOrReadOnly
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


class QuestionnaireTypeCreate(generics.ListCreateAPIView):
    queryset = QuestionnaireType.objects.all()
    serializer_class = QuestionnaireTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class QuestionnaireTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionnaireType.objects.all()
    serializer_class = QuestionnaireTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class SurveyAnalyse(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, survey_id, format=None):
        survey_result = {}
        survey = get_object_or_404(Survey, pk=survey_id)
        if survey.owner != request.user:
            message = {
                "detail": "You do not have permission to perform this action."
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN)
        survey_result['survey_id'] = survey.id
        survey_result['number_of_response'] = survey.number_of_response
        questionnaires = []

        for section in survey.sections.all():
            for questionnaire in section.questionnaires.all():
                questionnaire_result = {}
                questionnaire_result['questionnaire_id'] = questionnaire.id
                questionnaire_result['questionnaire_type'] = questionnaire.questionnaire_type.type_name
                questionnaire_result['title'] = questionnaire.title
                questionnaire_result['questionnaire_id'] = questionnaire.id

                if questionnaire_result['questionnaire_type'] in ['Multiple choice', 'Drop down', 'Check box']:
                    choice_serializer = ChoiceResponseSerializer(questionnaire.choices, many=True)
                    questionnaire_result['choices'] = choice_serializer.data
                elif questionnaire_result['questionnaire_type'] == 'Integer':
                    response_integer = []
                    for response in questionnaire.responses.all():
                        response_integer.append(response.response_integer)
                    questionnaire_result['integers'] = response_integer
                elif questionnaire_result['questionnaire_type'] == 'Decimal':
                    response_decimal = []
                    for response in questionnaire.responses.all():
                        response_decimal.append(response.response_decimal)
                    questionnaire_result['decimals'] = response_decimal
                elif questionnaire_result['questionnaire_type'] == 'Date':
                    response_date = []
                    for response in questionnaire.responses.all():
                        response_date.append(response.response_date)
                    questionnaire_result['responses'] = response_date
                elif questionnaire_result['questionnaire_type'] == 'Time':
                    response_time = []
                    for response in questionnaire.responses.all():
                        response_time.append(response.response_time)
                    questionnaire_result['responses'] = response_time
                else:
                    response_text = []
                    for response in questionnaire.responses.all():
                        response_text.append(response.response_text)
                    questionnaire_result['responses'] = response_text
                questionnaires.append(questionnaire_result)
        survey_result['questionnaires'] = questionnaires

        return Response(survey_result, status=status.HTTP_200_OK)