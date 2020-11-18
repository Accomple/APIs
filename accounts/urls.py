from django.urls import path
from .views import *

app_name = "accounts"
urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('verification_code/', CodeVerification.as_view(), name='code_verification'),
    path('verification_link/<str:path>/', LinkVerification.as_view(), name='link_verification'),
    path('validate_token/', ValidateToken.as_view(), name='validate_token'),
    path('get_profile/', GetProfile.as_view(), name='get_profile'),
    path('bookmark/add/building_id=<int:id>/', AddBookmark.as_view(), name='add_bookmark'),
    path('bookmarks/get/user=me/', MyBookmarks.as_view(), name='my_bookmarks'),
    path('bookmark/delete/id=<int:id>/', DeleteBookmark.as_view(), name='delete_bookmark'),
    path('profile/update/user=me/', UpdateProfile.as_view(), name='update_profile'),
    path('buildings/get/user=me/', RegisteredBuildings.as_view(), name="registered_building"),
    path('booking/get/user=me/', ActiveBooking.as_view(), name="active_booking"),
    path('password/update/user=me/', UpdatePassword.as_view(), name="update_password"),
    path('delete/user=me/', DeleteUser.as_view(), name="delete_user")
]
