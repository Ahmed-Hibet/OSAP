from rest_framework import serializers
from .models import (
    Survey, 
    Section, 
    Questionnaire, 
    QuestionnaireType, 
    Choice, 
    SurveyRequirement
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
            'id', 'title', 'description', 'has_dependency', 'is_required',
            'questionnaire_type', 'choices'
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
 