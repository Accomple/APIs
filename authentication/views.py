from django.shortcuts import render
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


import secrets


class Register(APIView):

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'detail': "logout required"}, status=status.HTTP_409_CONFLICT)

        context = {}
        user = CustomUserSerializer(data=request.data)

        if user.is_valid():
            user = user.save()
            serializer = CustomUserSerializer(user)
            context = serializer.data
            del (context['password'])
            token = Token.objects.create(user=user)
            token.save()
            context['token'] = token.key

            otp = OTP.objects.create(user=user)
            otp.generate()
            send_mail(
                'Accomple Registration',
                'OTP: ' + otp.key,
                settings.EMAIL_HOST_USER,
                [context['username'], settings.EMAIL_HOST_USER],
                fail_silently=True
            )
        else:
            context['detail'] = "serialization error"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        if user.is_owner:
            owner = Owner.objects.create(user=user)
            owner.save()
        else:
            seeker = Seeker.objects.create(user=user)
            seeker.save()

        return Response(context, status=status.HTTP_201_CREATED)


class Login(APIView):

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'detail': "logout required"}, status=status.HTTP_409_CONFLICT)

        context = {}
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            context['token'] = token.key
            context['is_owner'] = user.is_owner
            context['is_superuser'] = user.is_superuser
            login(request, user)
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['detail'] = 'Incorrect username or password'
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        # Delete Existing Token
        token = Token.objects.get(user=request.user)
        token.delete()
        # Create New Token
        token = Token.objects.create(user=request.user)
        token.save()
        logout(request)
        context['detail'] = 'logged out'
        return Response(context, status=status.HTTP_200_OK)
    # deletion of token @ front-end is required


class CodeVerification(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        context['email'] = request.user.username
        context['is_verified'] = request.user.is_verified
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_verified:
            return Response({'detail': "verified account"}, status=status.HTTP_423_LOCKED)

        if request.data['resend']:
            otp = OTP.objects.get(user=request.user)
            otp.generate()
            send_mail(
                'Accomple Registration',
                'OTP: ' + otp.key,
                settings.EMAIL_HOST_USER,
                [request.user.username, settings.EMAIL_HOST_USER],
                fail_silently=True
            )
            return Response({}, status=status.HTTP_201_CREATED)

        else:
            context = {'is_verified': False}
            key = request.data['otp']
            otp = OTP.objects.get(user=request.user)

            if key != otp.key:
                context['detail'] = "Invalid OTP"
                return Response(context, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            elif otp.is_expired():
                context['detail'] = "OTP expired"
                return Response(context, status=status.HTTP_410_GONE)

            else:
                request.user.is_verified = True
                request.user.save()
                context['is_verified'] = True
                context['detail'] = "OTP accepted, verification success"
                return Response(context, status=status.HTTP_202_ACCEPTED)


class LinkVerification(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, path):
        if request.user.is_verified:
            return Response({'detail': "verified account"}, status=status.HTTP_423_LOCKED)

        if path == request.user.email_verification_token:
            request.user.is_verified = True
            request.user.save()
            return Response({'detail': "account verification success"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'detail': "invalid email_verification_token"}, status=status.HTTP_406_NOT_ACCEPTABLE)

