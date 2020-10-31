import secrets

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


class AddBuilding(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        context = {}
        post_data = request.data.copy()

        building = BuildingSerializer(data=post_data)
        if building.is_valid():
            building = building.save()
            serializer = BuildingSerializer(building)
            context = serializer.data
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context['detail'] = "serialization error (Building)"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class AddRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        context = {}
        post_data = request.data.copy()

        owner = get_object_or_404(Owner, user=request.user)
        building = get_object_or_404(Building, id=id)
        post_data['owner'] = owner.id
        post_data['building'] = building.id

        room = RoomSerializer(data=post_data)
        if room.is_valid():
            room = room.save()
            serializer = RoomSerializer(room)
            context = serializer.data
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context['detail'] = "serialization error (Room)"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class AddDetails(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        context = {}
        post_data = request.data.copy()

        room = get_object_or_404(Room, id=id)
        for perk in post_data['perks']:
            Perk.objects.create(room=room, description=perk)
        context['detail'] = "success"
        return Response(context, status=status.HTTP_200_OK)


class AddPhotos(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        context = {}
        post_data = request.data.copy()

        room = get_object_or_404(Room, id=id)
        for photo in post_data.get('photos'):
            ext = photo.name.split('.')[-1]
            photo.name = str(room.id) + '.' + secrets.token_urlsafe(30) + '.' + ext
            RoomPhoto.objects.create(room=room, photo=photo)
        context['detail'] = "success"
        return Response(context, status=status.HTTP_200_OK)


class AddPropertyDeed(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        context = {}
        post_data = request.data.copy()

        room = get_object_or_404(Room, id=id)
        owner = room.owner
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


class DeletePerk(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request,id):
        context = {}
        perk = get_object_or_404(Perk,id=id)
        perk.delete()
        context['detail'] = "success"
        return Response(context, status=status.HTTP_200_OK)


class DeletePhoto(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        context = {}
        photo = get_object_or_404(RoomPhoto, id=id)
        photo.delete()
        context['detail'] = "success"
        return Response(context, status=status.HTTP_200_OK)


class Unbook(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        context = {}
        post_data = request.data.copy

        room = get_object_or_404(Room, id)
        if request.user.is_owner:
            if room.owner.user == request.user:
                room.is_booked = False
                room.save()
                context['detail'] = "success"
                return Response(context, status=status.HTTP_200_OK)
            else:
                context['detail'] = "Invalid User"
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)
        else:
            booking = get_object_or_404(Booking, room=room)
            seeker = booking.user
            if seeker.user == request.user:
                room.is_booked = False
                room.save()
                context['detail'] = "success"
                return Response(context, status=status.HTTP_200_OK)
            else:
                context['detail'] = "Invalid User"
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)


class RoomDetail(APIView):

    def get(self, request, id):
        context = {}
        room = get_object_or_404(Room, id=id)
        context = describe_room(query_set=room)
        return Response(context, status=status.HTTP_200_OK)


class RoomList(APIView):

    def get(self, request, filter=None):
        context = {}

        if filter is None:
            rooms = Room.objects.all()
            context = describe_room(query_set=rooms, many=True)
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)
