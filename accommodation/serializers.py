import secrets

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *


class BuildingSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Building
        fields = [
            'id',
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
            building_name=validated_data.get('building_name'),
            street=validated_data.get('street'),
            city=validated_data.get('city'),
            state=validated_data.get('state'),
            zip_code=validated_data.get('zip_code'),
            landmark=validated_data.get('landmark'),
            latitude=validated_data.get('latitude'),
            longitude=validated_data.get('longitude'),
            in_time=validated_data.get('in_time')
        )
        return building


class RoomSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = [
            'id',
            'owner',
            'building',
            'title',
            'rent',
            'room_no',
            'gender_label',
            'occupancy',
            'is_booked',
            'is_verified',
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
            is_verified=False,
            display_pic=display_pic
        )
        return room


class PropertyDeedSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = PropertyDeed
        fields = [
            'id',
            'room',
            'owner',
            'registration_no',
            'issue_date',
            'expiry_date',
            'document'
        ]
        validators = [UniqueTogetherValidator(queryset=PropertyDeed.objects.all(), fields=['registration_no', 'room'])]

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


class RoomPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPhoto
        read_only_fields = ['id', 'photo']
        fields = ['id', 'photo']


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        read_only_fields = ['id', 'description']
        fields = ['id', 'description']


def describe_room(query_set, many=False):
    if many:
        context = []
        for room in query_set:
            photos = RoomPhoto.objects.filter(room=room)
            perks = Perk.objects.filter(room=room)
            serialized_room = RoomSerializer(room)
            serialized_building = BuildingSerializer(room.building)
            serialized_photos = RoomPhotoSerializer(photos, many=True)
            serialized_perks = PerkSerializer(perks, many=True)
            serialized_data = {
                'room': serialized_room.data,
                'building': serialized_building.data,
                'photos': serialized_photos.data,
                'perks': serialized_perks.data
            }
            context.append(serialized_data)
    else:
        context = {}
        room = query_set
        photos = RoomPhoto.objects.filter(room=room)
        perks = Perk.objects.filter(room=room)
        serialized_room = RoomSerializer(room)
        serialized_building = BuildingSerializer(room.building)
        serialized_photos = RoomPhotoSerializer(photos, many=True)
        serialized_perks = PerkSerializer(perks, many=True)
        context['room'] = serialized_room.data
        context['building'] = serialized_building.data
        context['photos'] = serialized_photos.data
        context['perks'] = serialized_perks.data

    return context
