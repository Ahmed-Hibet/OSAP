from django.contrib import admin
from .models import (
    Survey,
    Section,
    QuestionnaireType,
    Questionnaire,
    Choice, Response,
    SurveyRequirement,
    Report,
    RespondentHistory,
)
# Register your models here.
admin.site.register(Survey)
admin.site.register(Section)
admin.site.register(QuestionnaireType)
admin.site.register(Questionnaire)
admin.site.register(Choice)
admin.site.register(SurveyRequirement)
admin.site.register(Report)
admin.site.register(RespondentHistory)