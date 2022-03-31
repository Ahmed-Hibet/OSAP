from django.urls import path
from .views import (
    EducationLevelCreate, EducationLevelDetail, 
    OccupationCreate, OccupationDetail
    )


urlpatterns = [
    path('requirements/education-levels/', EducationLevelCreate.as_view()),
    path('requirements/education-levels/<int:pk>', EducationLevelDetail.as_view()),
    path('requirements/occupations/', OccupationCreate.as_view()),
    path('requirements/occupations/<int:pk>', OccupationDetail.as_view()),
]
