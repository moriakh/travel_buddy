from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import Users, Trips
import datetime

# @login_required
def index(request):
    current_user = Users.objects.get(id = int(request.session['user']['id']))
    context = {
        'users' : Users.objects.all(),
        'own_trips' : current_user.own_trips,
        'user_trips' : Trips.objects.filter(user__id = current_user.id),
        'trips' : Trips.objects.exclude(owner_user__id = current_user.id) | Trips.objects.exclude(user__id = current_user.id),
    }

    return render(request, 'index.html', context)

# @login_required
def destination(request, trip_id):
    current_user = Users.objects.get(id = int(request.session['user']['id']))
    trip = Trips.objects.get(id = trip_id)

    context = {
        'trip' : trip
    }
    return render(request, 'destination.html', context)

# @login_required
def add_view(request):
    return render(request, 'add_trip.html')

# @login_required
def add_trip(request):
    if request.method == "POST":

        errors = Trips.objects.validate(request.POST)
        if len(errors) > 0:
            for key, value in errors:
                messages.error(request, value)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            trip = Trips.objects.create(destination = request.POST['destination'],
                                        start_date = datetime.datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date(),
                                        end_date = datetime.datetime.strptime(request.POST['end_date'], "%Y-%m-%d").date(),
                                        plan = request.POST['description_plan'])
            user = Users.objects.get(id = int(request.session['user']['id']))
            user.own_trips.add(trip)
            user.trips.add(trip)
            return redirect('/')
    else:
        return redirect(request.META.get('HTTP_REFERER'))

# @login_required
def travels(request, user_id):
    return redirect(request.META.get('HTTP_REFERER'))

# @login_required
def join_trip(request, trip_id):
    user = Users.objects.get(id = int(request.session['user']['id']))
    user.trips.add(Trips.objects.get(id = trip_id))
    return redirect(request.META.get('HTTP_REFERER'))