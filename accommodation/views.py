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


class RoomRegistration(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        context = {}
        post_data = request.data.copy()

        building = BuildingSerializer(data=post_data)
        if building.is_valid():
            building = building.save()
            serializer = BuildingSerializer(building)
            context['building'] = serializer.data

            owner = Owner.objects.get(user=request.user)
            post_data['owner'] = owner.id
            post_data['building'] = building.id
            room = RoomSerializer(data=post_data)

            if room.is_valid():
                room = room.save()
                serializer = RoomSerializer(room)
                context['room'] = serializer.data
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                building.delete()
                del context['building']
                context['detail'] = "serialization error (Room)"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        else:
            context['detail'] = "serialization error (Building)"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class RoomModification(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        context = {}
        post_data = request.data.copy()
        room = get_object_or_404(Room, id=id)
        owner = room.owner
        if get_object_or_404(Owner, user=request.user) != owner:
            context['detail'] = "owner didn't match"
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        post_data['owner'] = owner.id
        property_deed = PropertyDeedSerializer(data=post_data)
        if property_deed.is_valid():
            property_deed = property_deed.save()
            serializer = PropertyDeedSerializer(property_deed)
            context = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['detail'] = "Serialization Error (PropertyDeed)"

            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class RoomDetail(APIView):

    def get(self, request, id):
        context = {}
        room = get_object_or_404(Room, id=id)
        building = room.building
        serialized_room = RoomSerializer(room)
        serialized_building = BuildingSerializer(building)
        context['building'] = serialized_building.data
        context['room'] = serialized_room.data
        return Response(context, status=status.HTTP_200_OK)