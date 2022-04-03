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


class Section(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(help_text="Order of this section of the survey relative to other section. Lowest order number indicates the first section.")
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)


class QuestionnaireType(models.Model):
    type_name = models.CharField(max_length=50)


class Questionnaire(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    questionnaire_type = models.ForeignKey(QuestionnaireType, on_delete=models.PROTECT)
    has_dependency = models.BooleanField(default=False, help_text="Check whether next section can be determined depend upon this question")
    is_required = models.BooleanField(default=True)


class Choice(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    total_selected = models.IntegerField(default=0)
    next_section = models.ForeignKey(Section, on_delete=models.PROTECT, blank=True, null=True, help_text="If the question has dependence, the next section if this choice selected")


class Response(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    response = models.TextField()


class SurveyRequirement(models.Model):
    GENDER = [('Both', 'Both'), ('M', 'Male'), ('F', 'Female')]
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    minimum_age = models.IntegerField(blank=True, null=True)
    maximum_age = models.IntegerField(blank=True, null=True)
    occupations = models.ManyToManyField("access.Occupation")
    education_levels = models.ManyToManyField("access.EducationLevel")
    gender = models.CharField(choices=GENDER, max_length=5)
    allow_unverified_respondents = models.BooleanField(default=False)


class Report(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    message = models.TextField()
