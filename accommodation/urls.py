from django.urls import path
from .views import *

app_name = "accommodation"
urlpatterns = [
    path('add-building/', AddBuilding.as_view(), name='add_building'),
    path('add-room/<int:id>/', AddRoom.as_view(), name='add_room'),
    path('add-details/<int:id>/', AddDetails.as_view(), name='add_details'),
    path('add-photos/<int:id>/', AddPhotos.as_view(), name='add_photos'),
    path('add-property-deed/<int:id>/', AddPropertyDeed.as_view(), name='add_property_deed'),

    path('room-detail/<int:id>/', RoomDetail.as_view(), name='room_detail'),
    path('filter/<str:filter>/', RoomList.as_view()),
    path('', RoomList.as_view(), name='room_list'),
]