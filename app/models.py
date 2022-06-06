from lib2to3.pytree import Base
from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

import uuid

# Create your models here.


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add =True)                                        
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True                               



class Amenity(BaseModel):                                 
    amenity_name = models.CharField(max_length=120, unique=True, db_index=True)

    def __str__(self):
        return self.amenity_name



class Hotel(BaseModel):
    hotel_name = models.CharField(max_length=120, unique=True, db_index=True)
    booking_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], db_index=True)
    description = models.TextField(blank=True)
    amenities = models.ManyToManyField(Amenity, 'hotel_amenities')
    room_count = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(700)])
    phone = models.CharField(max_length=14, null=True, blank=True)

    def __str__(self):
        return self.hotel_name


class HotelImage(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True, related_name="hotel_images")        # yo line ko related_name attribute specifies the name of the reverse relation (i.e from the Hotel model to the HotelImage model Or we can say, from Parent table to Child table)     # if you give related_name to any foreign key, then this related_name will override the way how django provides default way to access child table from parent table (i.e parent.child_set.all() ,,, now you cannot do this, instead you have to do ==. parent.relate_name.all() )
    images = models.ImageField(upload_to='hotels/', null=True, blank=True, default='hotels/hotel_img.png') 

    def __str__(self):
        return str(self.images)


class HotelBooking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True, related_name='user_booking')       # yo line ko related_name attribute specifies the name of the reverse relation (i.e from the User model to the HotelBooking model Or we can say, from Parent table to Child table)     # if you give related_name to any foreign key, then this related_name will override the way how django provides default way to access child table from parent table (i.e parent.child_set.all() ,,, now you cannot do this, instead you have to do ==. parent.relate_name.all() )
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True, related_name="hotel_booking")
    check_in = models.DateField()
    check_out = models.DateField()

    booked_at = models.DateTimeField(auto_now_add =True)

    booking_type = models.CharField(max_length=20, choices=(('Pre Paid', 'Pre Paid'), ('Post Paid', 'Post Paid')))

    class Meta:
        ordering: ['-booked_at']
    
    def __str__(self):
        return str(self.check_in)+'-'+str(self.check_out) + ' ' + self.hotel.hotel_name

    





