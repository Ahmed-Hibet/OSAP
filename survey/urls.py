from django.urls import path
from .views import (
    SurveyCreate, 
    SurveyDetail,
    SurveyFill, 
    QuestionnaireTypeCreate, 
    QuestionnaireTypeDetail,
    SurveyAnalyse,
    SurveyReportCreate,
    SurveyReportDetail,
)

urlpatterns = [
    path('', SurveyCreate.as_view()),
    path('<int:pk>/', SurveyDetail.as_view()),
    path('fill/', SurveyFill.as_view()),
    path('questionnaire-types/', QuestionnaireTypeCreate.as_view()),
    path('questionnaire-types/<int:pk>/', QuestionnaireTypeDetail.as_view()),
    path('analyses/<int:survey_id>/', SurveyAnalyse.as_view()),
    path('reports/', SurveyReportCreate.as_view()),
    path('reports/<int:pk>/', SurveyReportDetail.as_view()),
]