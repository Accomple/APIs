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
            'area',
            'city',
            'state',
            'zip_code',
            'landmark',
            'latitude',
            'longitude',
            'gender_label',
            'display_pic',
            'in_time'
        ]

    def create(self, validated_data):
        display_pic = None
        if validated_data['display_pic']:
            display_pic = validated_data['display_pic']
            ext = display_pic.name.split('.')[-1]
            display_pic.name = secrets.token_urlsafe(30) + '.' + ext

        building = Building.objects.create(
            building_name=validated_data.get('building_name'),
            street=validated_data.get('street'),
            area=validated_data.get('area'),
            city=validated_data.get('city'),
            state=validated_data.get('state'),
            zip_code=validated_data.get('zip_code'),
            landmark=validated_data.get('landmark'),
            latitude=validated_data.get('latitude'),
            longitude=validated_data.get('longitude'),
            gender_label=validated_data.get('gender_label'),
            display_pic=display_pic,
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
            'description',
            'title',
            'rent',
            'total',
            'available',
            'occupancy',
            'is_verified',
        ]

    def create(self, validated_data):

        room = Room.objects.create(
            owner=validated_data['owner'],
            building=validated_data['building'],
            title=validated_data['title'],
            rent=validated_data['rent'],
            total=validated_data['total'],
            description=validated_data['description'],
            available=validated_data['available'],
            occupancy=validated_data['occupancy'],
            is_verified=False,
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
        validators = [
            UniqueTogetherValidator(queryset=PropertyDeed.objects.all(), fields=['registration_no']),
            UniqueTogetherValidator(queryset=PropertyDeed.objects.all(), fields=['room'])
        ]

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


class BuildingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingPhoto
        read_only_fields = ['id', 'caption', 'photo']
        fields = ['id', 'caption', 'photo']


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        read_only_fields = ['id', 'description']
        fields = ['id', 'description']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        read_only_fields = ['booking_no', 'room', 'user', 'booking_date']
        fields = ['booking_no', 'room', 'user', 'booking_date']



def describe_room(query_set, many=False):
    if many:
        context = []
        for room in query_set:
            photos = BuildingPhoto.objects.filter(room=room)
            perks = Perk.objects.filter(room=room)
            serialized_room = RoomSerializer(room)
            serialized_building = BuildingSerializer(room.building)
            serialized_photos = BuildingPhotoSerializer(photos, many=True)
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
        photos = BuildingPhoto.objects.filter(room=room)
        perks = Perk.objects.filter(room=room)
        serialized_room = RoomSerializer(room)
        serialized_building = BuildingSerializer(room.building)
        serialized_photos = BuildingPhotoSerializer(photos, many=True)
        serialized_perks = PerkSerializer(perks, many=True)
        context['room'] = serialized_room.data
        context['building'] = serialized_building.data
        context['photos'] = serialized_photos.data
        context['perks'] = serialized_perks.data

    return context
