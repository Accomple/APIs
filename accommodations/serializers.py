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
            'owner',
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
            owner=validated_data['owner'],
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

    def update(self, instance, validated_data):
        if validated_data.get('display_pic') != instance.display_pic:
            display_pic = validated_data.get('display_pic')
            ext = display_pic.name.split('.')[-1]
            display_pic.name = secrets.token_urlsafe(30) + '.' + ext
            validated_data['display_pic'] = display_pic
            instance.display_pic = validated_data.get('display_pic', instance.display_pic)

        instance.gender_label = validated_data.get('gender_label', instance.gender_label)
        instance.landmark = validated_data.get('landmark', instance.landmark)
        instance.in_time = validated_data.get('in_time', instance.in_time)
        instance.save()
        return instance


class RoomSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = [
            'id',
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

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.rent = validated_data.get('rent', instance.rent)
        instance.description = validated_data.get('description', instance.description)
        instance.occupancy = validated_data.get('occupancy', instance.occupancy)
        instance.save()
        return instance


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


class BookmarkSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Bookmark
        fields = [
            'id',
            'user',
            'building'
        ]
        validators = [
            UniqueTogetherValidator(queryset=Bookmark.objects.all(), fields=['user', 'building'])
        ]

    def create(self, validated_data):
        bookmark = Bookmark.objects.create(
            user=validated_data['user'],
            building=validated_data['building']
        )
        return bookmark
