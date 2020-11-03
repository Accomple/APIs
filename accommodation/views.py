import random
import secrets
import re
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import *
from .models import *
from apis import responses


class PostBuilding(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        context = {}
        post_data = request.data.copy()
        owner = get_object_or_404(Owner, user=request.user)
        post_data['owner'] = owner.id

        building = BuildingSerializer(data=post_data)
        if building.is_valid():
            building = building.save()
            serializer = BuildingSerializer(building)
            context = serializer.data
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context['detail'] = "serialization error (Building)"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class GetBuilding(APIView):

    def get(self, request, id):
        context = {}
        building = get_object_or_404(Building, id=id)
        context = responses.accommodation_detail(building)
        return Response(context, status=status.HTTP_200_OK)


class DeleteBuilding(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        context = {}
        building = get_object_or_404(Building, id=id)
        owner = building.owner
        if owner.user == request.user:
            building.delete()
            context['detail'] = "success"
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['detail'] = "invalid user"
            return Response(context, status=status.HTTP_409_CONFLICT)



class PostRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        context = {}
        post_data = request.data.copy()

        building = get_object_or_404(Building, id=id)
        owner = building.owner
        if owner.user != request.user:
            context['detail'] = "invalid user"
            return Response(context, status=status.HTTP_409_CONFLICT)

        post_data['building'] = building.id
        post_data['available'] = post_data['total']

        room = RoomSerializer(data=post_data)
        if room.is_valid():
            room = room.save()
            serializer = RoomSerializer(room)
            context = serializer.data
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context['detail'] = "serialization error (Room)"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class GetRoom(APIView):

    def get(self, request, id):
        context = {}
        room = get_object_or_404(Room, id=id)
        context = responses.room_detail(room)
        return Response(context, status=status.HTTP_200_OK)


class PostPerkList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        context = {}
        post_data = request.data.copy()

        building = get_object_or_404(Building, id=id)
        for description in post_data['perks']:
            perk, created = Perk.objects.get_or_create(description=description)
            perk.building.add(building)
        context['detail'] = "success"
        return Response(context, status=status.HTTP_200_OK)


class DeletePerk(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        context = {}
        perk = get_object_or_404(Perk, id=id)
        perk.delete()
        context['detail'] = "success"
        return Response(context, status=status.HTTP_200_OK)


class AddPhoto(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        context = {}
        post_data = request.data.copy()

        building = get_object_or_404(Building, id=id)
        photo = post_data.get('photo')
        ext = photo.name.split('.')[-1]
        photo.name = str(building.id) + '.' + secrets.token_urlsafe(30) + '.' + ext
        BuildingPhoto.objects.create(building=building, photo=photo)
        context['detail'] = "success"
        return Response(context, status=status.HTTP_200_OK)


class DeletePhoto(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        context = {}
        photo = get_object_or_404(BuildingPhoto, id=id)
        photo.delete()
        context['detail'] = "success"
        return Response(context, status=status.HTTP_200_OK)


class AddPropertyDeed(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        context = {}
        post_data = request.data.copy()

        room = get_object_or_404(Room, id=id)
        owner = room.building.owner
        post_data['room'] = room.id
        post_data['owner'] = owner.id

        property_deed = PropertyDeedSerializer(data=post_data)
        if property_deed.is_valid():
            property_deed = property_deed.save()
            serializer = PropertyDeedSerializer(property_deed)
            context = serializer.data
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context['detail'] = "serialization error (PropertyDeed)"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class GetPropertyDeed(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        context = {}
        property_deed = get_object_or_404(PropertyDeed, room__id=id)
        serializer = PropertyDeedSerializer(property_deed)
        context = serializer.data
        return Response(context, status=status.HTTP_200_OK)


class Book(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        context = {}
        room = get_object_or_404(Room, id=id)
        seeker = get_object_or_404(Seeker, user=request.user)

        if Booking.objects.filter(user=seeker).exists():
            context['detail'] = "duplicate user booking"
            return Response(context, status=status.HTTP_409_CONFLICT)

        if room.available <= 0:
            context['detail'] = "no rooms available"
            return Response(context, status=status.HTTP_409_CONFLICT)

        booking_no = ''.join(random.choice('0123456789') for _ in range(12))
        if room.available > 0:
            room.available -= 1
            room.save()
        else:
            context['detail'] = "no rooms available"
            return Response(context, status=status.HTTP_409_CONFLICT)

        booking = Booking.objects.create(user=seeker, room=room, booking_no=booking_no, booking_date=datetime.now())
        context = BookingSerializer(booking).data
        return Response(context, status=status.HTTP_201_CREATED)


class Unbook(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_no):
        context = {}

        booking = get_object_or_404(Booking, booking_no=booking_no)
        room = booking.room
        owner = room.building.owner
        if request.user.is_owner:
            if owner.user == request.user:
                booking.delete()
                if room.available < room.total:
                    room.available += 1
                    room.save()
                context['detail'] = "success"
                return Response(context, status=status.HTTP_200_OK)
            else:
                context['detail'] = "invalid user"
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)
        else:
            seeker = booking.user
            if seeker.user == request.user:
                booking.delete()
                if room.available < room.total:
                    room.available += 1
                    room.save()
                context['detail'] = "success"
                return Response(context, status=status.HTTP_200_OK)
            else:
                context['detail'] = "Invalid User"
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)


class AccommodationList(APIView):

    def get(self, request, filters=None):
        context = {}

        if filters is None:
            accommodations = Building.objects.all()
            context = responses.accommodation_list(accommodations)
            return Response(context, status=status.HTTP_200_OK)
        else:
            filters = filters.split("&")
            accommodations = Building.objects.all()

            for filter in filters:
                key = filter.split("=")[0]
                value = filter.split("=")[-1]
                if key == "city":
                    accommodations = accommodations & Building.objects.filter(city=value)
                elif key == "state":
                    accommodations = accommodations & Building.objects.filter(state=value)
                elif key == "search":
                    rooms = Room.objects.filter(description__contains=value) | Room.objects.filter(title__contains=value)
                    accommodations = accommodations & (Building.objects.filter(building_name__contains=value) | Building.objects.filter(room__in=rooms))
                elif key == "occupancy":
                    rooms = Room.objects.filter(occupancy=value)
                    accommodations = accommodations & Building.objects.filter(room__in=rooms)
                elif key == "rent_lte":
                    rooms = Room.objects.filter(rent__lte=value)
                    accommodations = accommodations & Building.objects.filter(room__in=rooms)
                elif key == "rent_gte":
                    rooms = Room.objects.filter(rent__gte=value)
                    accommodations = accommodations & Building.objects.filter(room__in=rooms)
                elif key == "gender_label":
                    accommodations = accommodations & Building.objects.filter(gender_label=value)
                else:
                    context['detail'] = "invalid filter format"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

            context = responses.accommodation_list(accommodations)
            return Response(context, status=status.HTTP_200_OK)
