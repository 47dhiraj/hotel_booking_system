from django.contrib import admin

from app.models import *

# Register your models here.

admin.site.register(Hotel)
admin.site.register(HotelBooking)
admin.site.register(HotelImage)
admin.site.register(Amenity)
