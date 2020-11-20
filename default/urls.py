from django.urls import path
from .views import *

app_name = "default"
urlpatterns = [
    path('active_cities/names/', ActiveCityNames.as_view(), name='active_city_names'),
    path('active_cities/zip_codes/', ActiveCityZipCodes.as_view(), name='active_city_zip_codes'),
]
