from django.urls import path
from .views import *

app_name = "accommodation"
urlpatterns = [
    path('add-building/', AddBuilding.as_view(), name='add_building'),
    path('add-room/<int:id>/', AddRoom.as_view(), name='add_room'),
    path('add-perks/<int:id>/', AddPerks.as_view(), name='add_perks'),
    path('add-photo/<int:id>/', AddPhoto.as_view(), name='add_photo'),
    path('add-property-deed/<int:id>/', AddPropertyDeed.as_view(), name='add_property_deed'),

    path('get-property-deed/<int:id>/', GetPropertyDeed.as_view(), name='get_property_deed'),

    path('book/<int:id>/', Book.as_view()),
    path('unbook/<str:booking_no>/', Unbook.as_view()),

    path('detail/<int:id>/', AccommodationDetail.as_view(), name='room_detail'),
    path('room/<int:id>/', RoomDetail.as_view()),
    path('<str:filters>/', AccommodationList.as_view()),
    path('', AccommodationList.as_view(), name='room_list'),
]