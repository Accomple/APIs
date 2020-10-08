import secrets

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            'is_verified',
            'phone_number',
            'is_owner',
            'date_of_birth',
            'is_superuser'
        ]

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email_verification_token=secrets.token_urlsafe(30),
            password_reset_token=secrets.token_urlsafe(30),
            phone_number=validated_data['phone_number'],
            date_of_birth=validated_data['date_of_birth'],
            is_owner=validated_data['is_owner']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

