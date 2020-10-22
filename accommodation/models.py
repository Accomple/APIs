from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.models import Owner, Seeker


class Building(models.Model):
    building_name = models.CharField(max_length=32)
    street = models.CharField(max_length=32)
    city = models.CharField(max_length=16)
    state = models.CharField(max_length=16)
    zip_code = models.CharField(max_length=6)
    landmark = models.CharField(max_length=32)
    latitude = models.FloatField()
    longitude = models.FloatField()
    in_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.building_name


class BuildingPerk(models.Model):
    building = models.ManyToManyField(Building)
    description = models.CharField(max_length=32)

    def __str__(self):
        return self.description


class Room(models.Model):
    GENDER_LABELS = [('M', 'Male'), ('F', 'Female'), ('U', 'Unisex')]

    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    rent = models.FloatField(null=False)
    room_no = models.IntegerField(null=False)
    gender_label = models.CharField(max_length=1, choices=GENDER_LABELS)
    occupancy = models.IntegerField()
    display_pic = models.ImageField(null=True, blank=True, upload_to='display_pics')
    is_booked = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class RoomPerk(models.Model):
    room = models.ManyToManyField(Room)
    description = models.CharField(max_length=32)

    def __str__(self):
        return self.description


class RoomPhoto(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='room_photos')

    def __str__(self):
        return self.photo.path


class Booking(models.Model):
    booking_no = models.CharField(max_length=32, unique=True)
    expiration = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(Seeker, on_delete=models.CASCADE)

    def __str__(self):
        return self.booking_no


class PropertyDeed(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    registration_no = models.CharField(max_length=32)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    document = models.FileField(upload_to='property_deeds')

    def __str__(self):
        return self.registration_no
