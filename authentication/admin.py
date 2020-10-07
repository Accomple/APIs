from django.contrib import admin

from .models import *

admin.site.register(CustomUser)
admin.site.register(OTP)
admin.site.register(Owner)
admin.site.register(Seeker)