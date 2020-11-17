from accommodations.models import *
from accommodations.serializers import *
from accounts.models import *
from accounts.serializers import *


def accommodation_list(accommodations):
    context = []
    for accommodation in accommodations:
        rooms = Room.objects.filter(building=accommodation, is_verified=True).order_by('rent')
        perks = Perk.objects.filter(building=accommodation)
        if rooms.exists():
            serialized_accommodation = BuildingSerializer(accommodation).data
            serialized_accommodation['starting_rent'] = rooms[0].rent
            serialized_accommodation['perks'] = PerkSerializer(perks, many=True).data
            context.append(serialized_accommodation)
    return context


def accommodation_detail(accommodation):
    context = BuildingSerializer(accommodation).data
    rooms = Room.objects.filter(building=accommodation, is_verified=True)
    perks = Perk.objects.filter(building=accommodation)
    photos = BuildingPhoto.objects.filter(building=accommodation)
    context['rooms'] = RoomSerializer(rooms, many=True).data
    context['photos'] = BuildingPhotoSerializer(photos, many=True).data
    context['perks'] = PerkSerializer(perks, many=True).data
    return context


def room_detail(room):
    context = RoomSerializer(room).data
    bookings = Booking.objects.filter(room=room)
    context['bookings'] = []
    for booking in bookings:
        seeker = booking.user
        context['bookings'].append(
            {
                'booking_no': booking.booking_no,
                'user': seeker.user.username,
                'first_name': seeker.user.first_name,
                'last_name': seeker.user.last_name,
                'phone_number': seeker.user.phone_number,
                'booking_date': booking.booking_date
            }
        )
    return context


def bookmark_list(bookmarks):
    context = BookmarkSerializer(bookmarks, many=True).data
    for bookmark in context:
        building_id = bookmark['building']
        building = Building.objects.filter(id=building_id)
        bookmark['building'] = accommodation_list(building)[0]
    return context
