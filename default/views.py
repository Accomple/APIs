from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accommodations.models import *


class ActiveCityNames(APIView):

    def get(self, request):
        context = {}
        cities_list = list(Building.objects.values_list('city', flat=True))
        cities_set = set()
        for city in cities_list:
            cities_set.add(str(city).capitalize())

        context = cities_set
        return Response(context, status=status.HTTP_200_OK)


class ActiveCityZipCodes(APIView):

    def get(self, request):
        context = {}
        zip_code_list = list(Building.objects.values_list('zip_code', flat=True))
        zip_code_set = set()
        for zip_code in zip_code_list:
            zip_code_set.add(int(zip_code))

        context = zip_code_set
        return Response(context, status=status.HTTP_200_OK)


def home(request):
    return redirect("https://github.com/Accomple/Documentation/blob/main/APIs.md")
