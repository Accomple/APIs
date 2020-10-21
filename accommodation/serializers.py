import secrets

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        field = [
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
        building.save()
        return building


    def update(self, instance, validated_data):
        instance.in_time = validated_data.get('in_time', instance.in_time)
        instance.landmark = validated_data.get('landmark', instance.landmark)
        instance.save()
        return instance

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        field = '__all__'

    def create(self, validated_data):
        room = Room.objects.create(
                building=validated_data['building'],
                owner=validated_data['owner'],
                title=validated_data['title'],
                rent=validated_data['rent'],
                room_no=validated_data['room_no'],
                gender_label=validated_data['gender_label'],
                occupancy=validated_data['occupancy'],
                display_pic=validated_data['display_pic'],
                is_booked=validated_data['is_booked']
        )
        room.save()
        return room


    def update(self, instance, validated_data):
        instance.title = validated_data.get('in_time', instance.title)
        instance.rent = validated_data.get('landmark', instance.rent)
        instance.gender_label = validated_data.get('gender_label', instance.gender_label)
        instance.occupancy = validated_data.get('occupancy', instance.occupancy)
        instance.display_pic = validated_data.get('display_pic', instance.display_pic)
        instance.is_booked = validated_data.get('is_booked', instance.is_booked)
        instance.save()
        return instance

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        field = '__all__'

    def create(self, validated_data):
        booking = Booking.objects.create(
            booking_no=validated_data['booking_no'],
            expiration=validated_data['building'],
            room=validated_data['room'],
            user=validated_data['user']
        )
        booking.save()
        return booking


    def update(self, instance, validated_data):
        instance.bookin_no = validated_data.get('in_time', instance.title)
        instance.user = validated_data.get('landmark', instance.rent)
        instance.save()
        return instance


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyDeed
        field = '__all__'
        validators = [UniqueTogetherValidator(queryset=PropertyDeed.objects.all(), fields=['registration_no'])]

    def create(self, validated_data):
        property = PropertyDeed.objects.create(
            owner=validated_data['owner'],
            room=validated_data['room'],
            registration_no=validated_data['registration_no'],
            issue_date=validated_data['issue_date'],
            expiry_date = validated_data['expiry_date'],
            document = validated_data['document']
        )
        property.save()
        return property

