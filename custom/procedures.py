import math
from threading import Thread
from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail


def merge(serialized_data, post_data):
    merged_data = post_data.copy()
    for key in serialized_data:
        if merged_data.get(key) is None:
            merged_data[key] = serialized_data[key]
    return merged_data


def haversine_distance(lat1, long1, lat2, long2):
    r = 6371.0710  # radius of earth in km
    rad_lat1 = lat1 * math.pi / 180
    rad_lat2 = lat2 * math.pi / 180
    lat_diff = rad_lat2 - rad_lat1
    long_diff = (long2 - long1) * math.pi / 180
    distance = 2 * r * math.asin(
        math.sqrt(
            math.sin(lat_diff / 2) * math.sin(lat_diff / 2) +
            math.cos(rad_lat1) * math.cos(rad_lat2) * math.sin(long_diff / 2) * math.sin(long_diff / 2)
        )
    )
    return distance


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def to_coordinates(value):
    if len(value.split(",")) != 2:
        return None
    lat = value.split(",")[0]
    long = value.split(",")[-1]
    if not is_float(long) or not is_float(lat):
        return None
    lat = float(lat)
    long = float(long)

    if (-180 <= long <= 180) and (-90 <= lat <= 90):
        return lat, long
    else:
        return None


class EmailThread(Thread):
    def __init__(self, email_to, subject, body):
        self.email_to = email_to
        self.subject = subject
        self.body = body
        Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.body,
            settings.EMAIL_HOST_USER,
            [self.email_to, settings.EMAIL_HOST_USER],
            fail_silently=True
        )


class MessageThread(Thread):

    def __init__(self, send_to, body):
        self.send_to = '+91'+str(send_to)
        self.body = body
        Thread.__init__(self)

    def run(self):

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=self.body,
            from_=settings.TWILIO_NUMBER,
            to=self.send_to
        )


def booking_added_mail(booking_no, building_name, room_title, user):
    body = "Hey!\nYou have a new booking #"+str(booking_no)
    body += "\nfor "+str(room_title)+" in "+str(building_name)+", by "+user
    return body


def booking_cancelled_mail(booking_no, building_name, room_title, owner=True):
    body = "Hello!\nYour Booking #"+str(booking_no)
    body += "\nfor "+str(room_title)+" in "+str(building_name)
    if owner:
        body += "\nhas been cancelled by the Owner"
    else:
        body += "\nhas been cancelled by the User"
    return body
