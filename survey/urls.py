from django.urls import path
from .views import (
    SurveyCreate, 
    SurveyFill, 
    QuestionnaireTypeCreate, 
    QuestionnaireTypeDetail,
    SurveyAnalyse,
)

urlpatterns = [
    path('', SurveyCreate.as_view()),
    path('fill/', SurveyFill.as_view()),
    path('questionnaire-types/', QuestionnaireTypeCreate.as_view()),
    path('questionnaire-types/<int:pk>/', QuestionnaireTypeDetail.as_view()),
    path('analyses/<int:survey_id>/', SurveyAnalyse.as_view()),
]