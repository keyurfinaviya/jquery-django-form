from .models import SignUp
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate
from rest_framework import serializers
from application.mixins import UserSerializer
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed, ValidationError


class SignUpSerializer(UserSerializer, serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'password',
            'first_name',
            'last_name',
            'email',
            )

        read_only_fields = ('is_staff', 'is_active', 'last_login', 'groups', 'user_permissions', 'is_superuser',
                            'last_update_userid', 'last_update_date')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def validate_password(password):
        if validate_password(password) is None:
            return password

    @staticmethod
    def validate_email(email):
        try:
            get_user_model().objects.get(email=email)
            raise ValidationError('A user already exists with this email')
        except get_user_model().DoesNotExist:
            pass

        return email

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)

        self.user = user

        create_profile(user)

        return user


class LoginSerializer(UserSerializer, serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = (
            'email',
            'password'
            )

    def validate(self, data):
        user = authenticate(
            self.context['request'],
            email=data.get('email'),
            password=data.get('password'),
        )

        self.user = user
        
        return data


class LoginSocialSerializer(UserSerializer, serializers.ModelSerializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    provider_id = serializers.CharField()

    class Meta:
        model = get_user_model()
        read_only_fields = ('is_staff', 'is_active', 'last_login', 'groups', 'user_permissions', 'is_superuser',
                            'last_update_userid', 'last_update_date')
        exclude = ('password',)

    def create(self, validated_data):
        user, _ = get_user_model().objects.update_or_create(
            email=self.validated_data.get('email'),
            defaults={
                'first_name': self.validated_data.get('first_name'),
                'last_name': self.validated_data.get('last_name'),
                'email': self.validated_data.get('email'),
                'provider_id': self.validated_data.get('provider_id'),
                'is_active': True
            }
        )
        self.user = user

        create_profile(user)


# class SignUpSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = SignUp
# 		fields = ['id', 'firstname', 'lastname', 'email', 'password']


# class LoginSerializer(serializers.Serializer):
#     email = serializers.CharField()
#     password = serializers.CharField()

#     class Meta:
#         fields = (
#             'email',
#             'password'
#             )

#     def validate(self, data):
#         user = authenticate(
#             self.context['request'],
#             email=data.get('email'),
#             password=data.get('password'),
#         )

#         self.user = user
        
#         return data
