from django.urls import path
from .views import SurveyCreate, SurveyFill

urlpatterns = [
    path('', SurveyCreate.as_view()),
    path('fill/', SurveyFill.as_view()),
]