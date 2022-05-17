from rest_framework import serializers
from .models import (
    Survey, 
    Section, 
    Questionnaire, 
    QuestionnaireType, 
    Choice, 
    SurveyRequirement,
    Response,
    RespondentHistory,
)
from access.models import User, Occupation, EducationLevel
from access.serializers import EducationLevelSerializer, OccupationSerializer
# from djoser.serializers import UserSerializer
from access.serializers import UserCreateSerializer
from django.shortcuts import get_object_or_404


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'name', 'next_section']


class QuestionnaireTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireType
        fields = ['id', 'type_name']


class QuestionnaireSerializer(serializers.ModelSerializer):
    questionnaire_type = QuestionnaireTypeSerializer()
    choices = ChoiceSerializer(many=True)
    class Meta:
        model = Questionnaire
        fields = [
            'id', 
            'title', 
            'description', 
            'has_dependency', 
            'is_required',
            'questionnaire_type', 
            'choices', 
            'maximum_choice',
            'minimum_integer_value',
            'maximum_integer_value',
            'minimum_decimal_value',
            'maximum_decimal_value',
        ]
        # depth=1


class SectionSerializer(serializers.ModelSerializer):
    questionnaires = QuestionnaireSerializer(many=True)
    class Meta:
        model = Section
        fields = [
            'id', 'title', 'description', 'order', 'questionnaires'
        ]


class SurveyRequirementSerializer(serializers.ModelSerializer):
    occupations = OccupationSerializer(many=True)
    education_levels = EducationLevelSerializer(many=True)
    class Meta:
        model = SurveyRequirement
        fields = [
            'id', 
            'minimum_age', 
            'maximum_age', 
            'education_levels', 
            'occupations', 
            'gender', 
            'allow_unverified_respondents'
        ]
        depth = 1


class SurveySerializer(serializers.ModelSerializer):
    owner = UserCreateSerializer(read_only=True)
    sections = SectionSerializer(many=True)
    requirements = SurveyRequirementSerializer()
    class Meta:
        model = Survey
        fields = [
            'id', 'title', 'description', 'owner', 'budget', 'required_number_of_respondent', 
            'number_of_response', 'is_paid', 'is_active', 'created_at', 'expired_date',
            'sections', 'requirements'
        ]
        # depth = 2

    def create_questionnaires(self, questionnaires, section):
        for questionnaire in questionnaires:
            choices = questionnaire.pop('choices')
            questionnaire_type_name = questionnaire.pop('questionnaire_type')['type_name']
            questionnaire_type = QuestionnaireType.objects.filter(type_name=questionnaire_type_name).first()

            questionnaire = Questionnaire.objects.create(
                section=section, 
                questionnaire_type=questionnaire_type, 
                **questionnaire
            )
            
            for choice in choices:
                choice = Choice.objects.create(questionnaire=questionnaire, **choice)

    def create_sections(self, sections, survey):
        for section in sections:
            questionnaires = section.pop('questionnaires')
            section = Section.objects.create(survey=survey, **section)

            self.create_questionnaires(questionnaires, section)

        return survey
    
    def get_list_of_occupations_instance(self, occupations):
        list_of_occupations = []
        for occupation in occupations:
            work_type = occupation['work_type']
            occupation = Occupation.objects.filter(work_type=work_type).first()
            list_of_occupations.append(occupation)
        return list_of_occupations
    
    def get_list_of_education_levels_instance(self, education_levels):
        list_of_education_levels = []
        for education_level in education_levels:
            level_name = education_level['level_name']
            education_level = EducationLevel.objects.filter(level_name=level_name).first()
            list_of_education_levels.append(education_level)
        return list_of_education_levels

    def create_requirement(self, requirements, survey):
        education_levels = requirements.pop('education_levels')
        occupations = requirements.pop('occupations')

        requirements = SurveyRequirement.objects.create(survey=survey, **requirements)

        list_of_occupations = self.get_list_of_occupations_instance(occupations)
        requirements.occupations.set(list_of_occupations)

        list_of_education_levels = self.get_list_of_education_levels_instance(education_levels)
        requirements.education_levels.set(list_of_education_levels)
        
        requirements.save()
        return survey

    def create(self, validated_data):
        sections = validated_data.pop('sections')
        requirements = validated_data.pop('requirements')
        survey = Survey.objects.create(**validated_data)

        survey = self.create_sections(sections, survey)
        survey = self.create_requirement(requirements, survey)

        return survey
 
 
class ResponseSerializer(serializers.Serializer):
    questionnaire_id = serializers.IntegerField(min_value=1)
    response_choice = ChoiceSerializer(many=True)
    response_date = serializers.DateField(required=False, allow_null=True)
    response_time = serializers.TimeField(required=False, allow_null=True)
    response_text = serializers.CharField(required=False, allow_null=True)
    response_integer = serializers.IntegerField(required=False, allow_null=True)
    response_decimal = serializers.FloatField(required=False, allow_null=True)


class SurveyFillSerializer(serializers.Serializer):
    survey_id = serializers.IntegerField(min_value=1)
    responses = ResponseSerializer(many=True)

    def validate_responses(self, responses):
        for response in responses:
            questionnaire = get_object_or_404(Questionnaire, pk=response['questionnaire_id'])
            questionnaire_type = questionnaire.questionnaire_type.type_name
            if questionnaire_type == 'Check box' or questionnaire_type == 'Drop down':
                if questionnaire.maximum_choice < len(response['response_choice']):
                    raise serializers.ValidationError("response exceed the maximum limit")
            if questionnaire_type == 'Multiple choice':
                if len(response['response_choice']) > 1:
                    raise serializers.ValidationError("Only one choice is allowed")
            if questionnaire_type == 'Integer':
                if not(
                    questionnaire.minimum_integer_value <= response['response_integer'] and 
                    response['response_integer'] <= questionnaire.maximum_integer_value):
                        raise serializers.ValidationError("the number is out of range")
            if questionnaire_type == 'Decimal':
                if not(
                    questionnaire.minimum_decimal_value <= response['response_decimal'] and 
                    response['response_decimal'] <= questionnaire.maximum_decimal_value):
                        raise serializers.ValidationError("the number is out of range")                
        return responses

    def create(self, validated_data):
        survey = get_object_or_404(Survey, pk=validated_data['survey_id'])
        for response in validated_data['responses']:
            questionnaire = get_object_or_404(Questionnaire, pk=response['questionnaire_id'])
            questionnaire_type = questionnaire.questionnaire_type.type_name
            if questionnaire_type == 'Check box' or questionnaire_type == 'Drop down':
                for choice in response['response_choice']:
                    choice = Choice.objects.filter(questionnaire=questionnaire, name=choice["name"]).first()
                    choice.total_selected += 1
                    choice.save()
                
            elif questionnaire_type == 'Multiple choice':
                if response['response_choice']:
                    choice_obj = response['response_choice'][0]
                    choice = Choice.objects.filter(questionnaire=questionnaire, name=choice_obj["name"]).first()
                    choice.total_selected += 1
                    choice.save()

            elif questionnaire_type == 'Date':
                if response['response_date']:
                    response_obj = Response.objects.create(
                        questionnaire=questionnaire, 
                        response_date=response['response_date']
                    )
            elif questionnaire_type == 'Time':
                if response['response_time']:
                    response_obj = Response.objects.create(
                        questionnaire=questionnaire, 
                        response_time=response['response_time']
                    )
            elif questionnaire_type == 'Integer':
                if response['response_integer']:
                    response_obj = Response.objects.create(
                        questionnaire=questionnaire, 
                        response_integer=response['response_integer']
                    )
            elif questionnaire_type == 'Decimal':
                if response['response_decimal']:
                    response_obj = Response.objects.create(
                        questionnaire=questionnaire, 
                        response_decimal=response['response_decimal']
                    )
            else:
                if response['response_text']:
                    response_obj = Response.objects.create(
                        questionnaire=questionnaire, 
                        response_text=response['response_text']
                    )
        """
        Increase number of respondent for this survey and clear the
        is_active flag if it reaches the maximum limit
        """
        survey.number_of_response += 1
        if survey.number_of_response >= survey.required_number_of_respondent:
            survey.is_active = False
        survey.save()

        """
        Create a respondent history       
        """
        user = User.objects.get(pk=validated_data['respondent'].id)
        respondent_history = RespondentHistory.objects.create(
            respondent=user, 
            survey=survey
        )

        if survey.is_paid:
            user.balance += survey.budget//survey.required_number_of_respondent
            user.save()
        return validated_data
