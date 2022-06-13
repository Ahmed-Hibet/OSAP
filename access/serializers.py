from djoser.serializers import UserCreateSerializer
from access.models import User
from rest_framework import serializers
from access.models import User, EducationLevel, Occupation

class UserCreateSerializer(UserCreateSerializer):
    roll = serializers.SlugRelatedField(
        read_only=True,
        slug_field='roll_name'
    )
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password', 'roll', 'balance']


class RespondentSerializer(UserCreateSerializer):
    roll = serializers.SlugRelatedField(
        read_only=True,
        slug_field='roll_name'
    )
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            'id', 
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'gender', 
            'birth_date', 
            'region', 
            'city', 
            'phone_number', 
            'education_level', 
            'occupation', 
            'password',
            'roll',
            'balance',
        ]


class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = ['id', 'level_name', 'description']


class OccupationSerializer(serializers.ModelSerializer):
     class Meta:
        model = Occupation
        fields = ['id', 'work_type', 'description']