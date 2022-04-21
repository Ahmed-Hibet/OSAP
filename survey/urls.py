from django.urls import path
from .views import SurveyCreate

urlpatterns = [
    path('', SurveyCreate.as_view()),
]