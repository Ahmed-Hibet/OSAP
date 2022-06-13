from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey("access.User", on_delete=models.CASCADE)
    budget = models.IntegerField(default=0)
    required_number_of_respondent = models.IntegerField()
    number_of_response = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    expired_date = models.DateField(help_text="The date the survey becomes inactive")

    def __str__(self):
        return self.title
    

class Section(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(help_text="Order of this section of the survey relative to other section. Lowest order number indicates the first section.")
    survey = models.ForeignKey(Survey, related_name='sections', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class QuestionnaireType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name


class Questionnaire(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    section = models.ForeignKey(Section, related_name='questionnaires', on_delete=models.CASCADE)
    questionnaire_type = models.ForeignKey(QuestionnaireType, related_name='questionnaires', on_delete=models.PROTECT)
    maximum_choice = models.PositiveIntegerField(default=1, blank=True, null=True)
    minimum_integer_value = models.IntegerField(blank=True, null=True, help_text="only for questionnaire type of integer")
    maximum_integer_value = models.IntegerField(blank=True, null=True, help_text="only for questionnaire type of integer")
    minimum_decimal_value = models.FloatField(blank=True, null=True, help_text="only for questionnaire type of decimal")
    maximum_decimal_value = models.FloatField(blank=True, null=True, help_text="only for questionnaire type of decimal")
    has_dependency = models.BooleanField(default=False, help_text="Check whether next section can be determined depend upon this question")
    is_required = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Choice(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, related_name='choices', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    total_selected = models.IntegerField(default=0)
    next_section = models.PositiveIntegerField(blank=True, null=True, help_text="If the question has dependence, the next section order number if this choice selected")

    def __str__(self):
        return self.name


class Response(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, related_name='responses', on_delete=models.CASCADE)
    response_text = models.TextField(blank=True, null=True)
    response_date = models.DateField(blank=True, null=True)
    response_time = models.TimeField(blank=True, null=True)
    response_integer = models.IntegerField(blank=True, null=True)
    response_decimal = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.questionnaire.title


class SurveyRequirement(models.Model):
    GENDER = [('Both', 'Both'), ('M', 'Male'), ('F', 'Female')]
    survey = models.OneToOneField(Survey, related_name='requirements', on_delete=models.CASCADE)
    minimum_age = models.IntegerField(blank=True, null=True)
    maximum_age = models.IntegerField(blank=True, null=True)
    occupations = models.ManyToManyField("access.Occupation")
    education_levels = models.ManyToManyField("access.EducationLevel")
    gender = models.CharField(choices=GENDER, max_length=5)
    allow_unverified_respondents = models.BooleanField(default=False)

    def __str__(self):
        return self.survey.title
    

class Report(models.Model):
    survey = models.ForeignKey(Survey, related_name='reports', on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.survey.title


class RespondentHistory(models.Model):
    respondent = models.ForeignKey("access.User", related_name="survey_history", on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, related_name="survey_history", on_delete=models.CASCADE)

    def __str__(self):
        return self.respondent.username + ": " + self.survey.title