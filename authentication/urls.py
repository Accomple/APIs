from django.urls import path
from .views import *

app_name = "authentication"
urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('verification_code/', CodeVerification.as_view(), name='code_verification'),
    path('verification_link/<str:path>/', LinkVerification.as_view(), name='link_verification'),

]