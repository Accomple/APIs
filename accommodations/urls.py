from django.urls import path
from .views import *

app_name = "accommodations"
urlpatterns = [
    path('building/add/', AddBuilding.as_view(), name='add_building'),
    path('room/add/building_id=<int:id>/', AddRoom.as_view(), name='add_room'),
    path('perks/add/building_id=<int:id>/', AddPerks.as_view(), name='add_perks'),
    path('photo/add/building_id=<int:id>/', AddPhoto.as_view(), name='add_photo'),
    path('property-deed/add/room_id=<int:id>/', AddPropertyDeed.as_view(), name='add_property_deed'),
    path('booking/add/id=<int:id>/', AddBooking.as_view(), name='add_booking'),

    path('building/get/id=<int:id>/', GetBuilding.as_view(), name='get_building'),
    path('room/get/id=<int:id>/', GetRoom.as_view(), name='get_room'),
    path('property-deed/get/id=<int:id>/', GetPropertyDeed.as_view(), name='get_property_deed'),

    path('delete/id=<int:id>/', DeleteBuilding.as_view(), name='delete_building'),
    path('booking/delete/id=<str:booking_no>/', DeleteBooking.as_view(), name='delete_booking'),

    path('<str:filters>/', AccommodationList.as_view()),
    path('', AccommodationList.as_view(), name='room_list'),
]