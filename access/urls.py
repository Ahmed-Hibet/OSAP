from django.urls import path
from .views import (
    EducationLevelCreate, 
    EducationLevelDetail, 
    OccupationCreate, 
    OccupationDetail,
    UserCreate,
    UserDetail,
    RespondentCreate,
)


urlpatterns = [
    path('requirements/education-levels/', EducationLevelCreate.as_view()),
    path('requirements/education-levels/<int:pk>/', EducationLevelDetail.as_view()),
    path('requirements/occupations/', OccupationCreate.as_view()),
    path('requirements/occupations/<int:pk>/', OccupationDetail.as_view()),
    path('auth/users/', UserCreate.as_view()),
    path('auth/users/me/', UserDetail.as_view()),
    path('auth/users/respondents/', RespondentCreate.as_view()),

]
