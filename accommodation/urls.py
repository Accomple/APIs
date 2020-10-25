from django.urls import path
from .views import *

app_name = "accommodation"
urlpatterns = [
    path('room-registration/', RoomRegistration.as_view(), name='room_registration'),
    path('room-modification/<int:id>/', RoomModification.as_view(), name='room_modification'),
    path('room-detail/<int:id>/', RoomDetail.as_view(), name='room_detail'),
    path('filter/<str:filter>/', RoomList.as_view()),
    path('', RoomList.as_view(), name='room_list'),
]