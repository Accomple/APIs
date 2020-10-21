import secrets

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = [
            'building_name',
            'street',
            'city',
            'state',
            'zip_code',
            'landmark',
            'latitude',
            'longitude',
            'in_time'
        ]

    def create(self, validated_data):
        building = Building.objects.create(
            building_name=validated_data['building_name'],
            street=validated_data['street'],
            city=validated_data['city'],
            state=validated_data['state'],
            zip_code=validated_data['zip_code'],
            landmark=validated_data['landmark'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            in_time=validated_data['in_time']
        )
        return building


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'owner',
            'building',
            'title',
            'rent',
            'room_no',
            'gender_label',
            'occupancy',
            'is_booked',
            'display_pic'
        ]

    def create(self, validated_data):
        display_pic = None
        if validated_data['display_pic']:
            display_pic = validated_data['display_pic']
            ext = display_pic.name.split('.')[-1]
            display_pic.name = secrets.token_urlsafe(30) + '.' + ext

        room = Room.objects.create(
            owner=validated_data['owner'],
            building=validated_data['building'],

            title=validated_data['title'],
            rent=validated_data['rent'],
            room_no=validated_data['room_no'],
            gender_label=validated_data['gender_label'],
            occupancy=validated_data['occupancy'],
            is_booked=False,
            display_pic=display_pic
        )
        return room


class PropertyDeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDeed
        fields = [
            'room',
            'owner',
            'registration_no',
            'issue_date',
            'expiry_date',
            'document'
        ]
        validators = [UniqueTogetherValidator(queryset=PropertyDeed.objects.all(), fields=['registration_no'])]

    def create(self, validated_data):
        document = None
        if validated_data['document']:
            document = validated_data['document']
            ext = document.name.split('.')[-1]
            document.name = secrets.token_urlsafe(30) + '.' + ext

        property_deed = PropertyDeed.objects.create(
            room=validated_data['room'],
            owner=validated_data['owner'],

            registration_no=validated_data['registration_no'],
            issue_date=validated_data['issue_date'],
            expiry_date=validated_data['expiry_date'],
            document=document
        )
        return property_deed
