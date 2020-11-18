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
from accommodations.models import Building
from custom import responses
from custom.procedures import *

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
            context['is_verified'] = user.is_verified
            context['name'] = user.first_name+" "+user.last_name
            login(request, user)
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['detail'] = 'Incorrect username or password'
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        # # Delete Existing Token
        # token = Token.objects.get(user=request.user)
        # token.delete()
        # # Create New Token
        # token = Token.objects.create(user=request.user)
        # token.save()
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


class ValidateToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        context['details'] = "ok"
        return Response(context, status=status.HTTP_200_OK)


class GetProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        user = request.user
        context = CustomUserSerializer(user).data
        del context['password']
        return Response(context, status=status.HTTP_200_OK)


class AddBookmark(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        context = {}
        post_data = request.data.copy()
        seeker = get_object_or_404(Seeker, user=request.user)
        building = get_object_or_404(Building, id=id)
        post_data['user'] = seeker.id
        post_data['building'] = building.id
        bookmark = BookmarkSerializer(data=post_data)
        if bookmark.is_valid():
            bookmark = bookmark.save()
            serializer = BookmarkSerializer(bookmark)
            context = serializer.data
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context['detail'] = "serialization error (Building)"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class MyBookmarks(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        seeker = get_object_or_404(Seeker, user=request.user)
        bookmarks = Bookmark.objects.filter(user=seeker)
        context = responses.bookmark_list(bookmarks)
        return Response(context, status=status.HTTP_200_OK)


class DeleteBookmark(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        context = {}
        bookmark = get_object_or_404(Bookmark, id=id)
        seeker = bookmark.user
        if seeker.user == request.user:
            bookmark.delete()
            context['detail'] = "success"
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['detail'] = "invalid user"
            return Response(context, status=status.HTTP_409_CONFLICT)


class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        context = {}
        post_data = request.data.copy()
        user = request.user
        if post_data.get('profile_pic') is None or post_data.get('profile_pic') == '':
            post_data['profile_pic'] = user.profile_pic

        post_data = merge(serialized_data=CustomUserSerializer(user).data, post_data=post_data)
        user = CustomUserSerializer(user, data=post_data)

        if user.is_valid():
            user.save()
            context = user.data
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['detail'] = "serialization error (User)"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class RegisteredBuildings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        owner = get_object_or_404(Owner, user=request.user)
        buildings = Building.objects.filter(owner=owner)
        context = BuildingSerializer(buildings, many=True).data
        return Response(context, status=status.HTTP_200_OK)


class ActiveBooking(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        seeker = get_object_or_404(Seeker, user=request.user)

        if Booking.objects.filter(user=seeker).exists():
            booking = get_object_or_404(Booking, user=seeker)
            context = responses.booking_details(booking=booking)
            context['exists'] = True
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['exists'] = False
            return Response(context, status=status.HTTP_200_OK)