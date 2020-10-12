from django.db import models

# Create your models here.
# from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.models import Owner


class Building(models.Model):
    building_name = models.CharField(max_length=20)
    coordinate_x = models.DoubleField(null=False)
    coordinate_y = models.DoubleField(null=False)
    landmark = models.CharField(max_length=40)
    in_time = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=40)

    def __str__(self):
        return self.id

class Building_Perks(models.Model):
    id=models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=40)
    building = models.ManyToManyField(Building, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.building.id

class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    title= models.CharField(max_length=40)
    rent = models.DoubleField(null=False)
    room_no=models.IntegerField(null=False)
    main_pic=models.ImageField(null=True, blank=True, upload_to='main_photo')
    description =models.CharField(max_length=40)
    owner=models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.id

class Room_Perks(models.Model):
    description = models.CharField(max_length=40)
    room = models.ManyToManyField(Room, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.room.id

class Room_Photos(models.Model):
    photo = models.ImageField(null=True, blank=True, upload_to='room_photo')
    room= models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

