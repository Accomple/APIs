import secrets

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *
from accommodations.serializers import *


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
            'is_superuser',
            'profile_pic'
        ]
        validators = [
            UniqueTogetherValidator(queryset=CustomUser.objects.all(), fields=['username'])
        ]

    def create(self, validated_data):
        profile_pic = None
        if validated_data['profile_pic']:
            profile_pic = validated_data['profile_pic']
            ext = profile_pic.name.split('.')[-1]
            profile_pic.name = secrets.token_urlsafe(30) + '.' + ext

        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email_verification_token=secrets.token_urlsafe(30),
            password_reset_token=secrets.token_urlsafe(30),
            phone_number=validated_data['phone_number'],
            date_of_birth=validated_data['date_of_birth'],
            is_owner=validated_data['is_owner'],
            profile_pic=profile_pic
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if validated_data.get('profile_pic') != instance.profile_pic:
            profile_pic = validated_data.get('profile_pic')
            ext = profile_pic.name.split('.')[-1]
            profile_pic.name = secrets.token_urlsafe(30) + '.' + ext
            validated_data['profile_pic'] = profile_pic
            instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)

        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
