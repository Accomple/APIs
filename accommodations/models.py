from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.models import Owner, Seeker


class Building(models.Model):
    GENDER_LABELS = [('M', 'Male'), ('F', 'Female'), ('U', 'Unisex')]
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    building_name = models.CharField(max_length=32)
    street = models.CharField(max_length=32)
    area = models.CharField(max_length=32)
    city = models.CharField(max_length=16)
    state = models.CharField(max_length=16)
    zip_code = models.CharField(max_length=6)
    landmark = models.CharField(max_length=32)
    latitude = models.FloatField()
    longitude = models.FloatField()
    gender_label = models.CharField(max_length=1, choices=GENDER_LABELS)
    display_pic = models.ImageField(upload_to='building_pics')
    in_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.building_name


class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    description = models.TextField()
    rent = models.FloatField(null=False)
    total = models.IntegerField(null=False)
    available = models.IntegerField(null=False)
    occupancy = models.IntegerField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Perk(models.Model):
    building = models.ManyToManyField(Building)
    description = models.TextField()

    def __str__(self):
        return self.description


class BuildingPhoto(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    caption = models.CharField(max_length=256, null=True, blank=True)
    photo = models.ImageField(upload_to='building_pics')

    def __str__(self):
        return self.photo.path


class Booking(models.Model):
    booking_no = models.CharField(max_length=32, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(null=True, blank=True)
    
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
