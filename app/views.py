from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from .models import Hotel, HotelBooking, Amenity

from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import (Amenity, Hotel, HotelBooking, HotelImage, )

from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.db.models import Q

from datetime import date
from datetime import datetime



# Create your views here.

def home(request):

    amenities = Amenity.objects.all()
    hotels = Hotel.objects.all()
    
    sort_by = request.GET.get('sort_by')
    search_query = request.GET.get('search')

    sort_amenities = request.GET.getlist('amenities')     


    if search_query:
        hotels = Hotel.objects.filter(Q(hotel_name__icontains=search_query) | Q(description__icontains=search_query)).distinct()  

    if len(sort_amenities):
        hotels = hotels.filter(amenities__amenity_name__in = sort_amenities).distinct() 

    if sort_by:
        sort_by = request.GET.get('sort_by')
        if sort_by == 'ASC':
            hotels = hotels.order_by('booking_price')
        elif sort_by == 'DSC':
            hotels = hotels.order_by('-booking_price')

    print(sort_by)

    context = {'amenities': amenities, 'hotels': hotels, 'sort_by': sort_by, 'search': search_query, 'sort_amenities': sort_amenities}
    return render(request, 'app/home.html', context)


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == '':
            messages.add_message(request, messages.ERROR, 'Username is required')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if password == '':
            messages.add_message(request, messages.ERROR, 'Password is required')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        user = authenticate(request, username=username, password=password)
        # print('User instance : ',user)


        if not user:
            messages.add_message(request, messages.ERROR, 'Invalid login credentials !')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        login(request, user)
        return redirect('/')

    return render(request, 'app/login.html')



def register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(username) < 3:
            messages.add_message(request, messages.ERROR, 'username must be 3 characters long')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if len(password) < 6 or len(password2) < 6:
            messages.add_message(request, messages.ERROR, 'passwords must be minimum of 6 characters')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if password != password2:
            messages.add_message(request, messages.ERROR, 'passwords doesn\'t match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

        try:
            user_obj = User.objects.get(username=username)
            if user_obj.exists():
                messages.add_message(request, messages.ERROR, 'user with that username already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        except Exception as e:
            pass

        try:
            user = User.objects.create(username=username, password=password)
            user.set_password(password)
            user.save()

            return redirect('login')

        except:
            messages.add_message(request, messages.ERROR, 'Something went wrong!')

    return render(request, 'app/register.html')




def check_booking(uid, room_count, checkin=None, checkout=None):

    bookings = HotelBooking.objects.filter(
        hotel__uid = uid,                               
        check_in__lte = checkin,
        check_out__gte = checkin
    )

    if len(bookings) >= room_count:
        return False

    rooms_available = room_count - len(bookings)
    return rooms_available



def detail(request,  uid):
    hotel = get_object_or_404(Hotel, uid=uid)

    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')

        try:
            today_date = datetime.now().date()
            checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
            checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()

            if checkin_date < today_date or checkout_date < today_date:
                messages.warning(request, 'CheckIn/CheckOut for past dates is not valid')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if checkin_date > checkout_date:
                messages.warning(request, 'CheckOut date cannot be ahead of CheckIn  !')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if checkin == checkout:
                messages.warning(request, 'CheckIn and CheckOut dates cannot be same !')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            messages.warning(request, 'Invalid CheckIn/CheckOut dates format !')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        rooms_available = check_booking(uid, hotel.room_count, checkin, checkout)

        if not rooms_available:
            messages.warning(request, 'Hotel is already booked for these CheckIn dates!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        hotel_booking = HotelBooking.objects.create(hotel=hotel, user=request.user, check_in=checkin, check_out=checkout, booking_type='Pre Paid')
        rooms_available -= 1

        messages.success(request, 'Booking of hotel has been made successfully !')
        # return render(request, 'app/hotel_detail.html', {'hotel': hotel})
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    return render(request, 'app/hotel_detail.html', {'hotel': hotel})

