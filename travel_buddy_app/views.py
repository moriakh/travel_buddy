from pdb import set_trace
from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import Users, Trips
from django.db.models import Q
import datetime

@login_required
def index(request):
    current_user = Users.objects.get(id = int(request.session['user']['id']))
    context = {
        'user_trips' : Trips.objects.filter(user__id = current_user.id),
        'trips' : Trips.objects.filter(~Q(user__id = current_user.id)),
    }
    return render(request, 'index.html', context)

@login_required
def destination(request, trip_id):
    current_user = Users.objects.get(id = int(request.session['user']['id']))
    trip = Trips.objects.get(id = trip_id)
    '''travellers = trip.user.all()
    travellers_id = [traveller.id for traveller in travellers]
    not_owner = [traveller for traveller in travellers if current_user.id not in travellers_id]'''
    travellers = trip.user.all().exclude(id = trip.owner_user.id)

    context = {
        'trip' : trip,
        'travellers' : travellers
    }
    return render(request, 'destination.html', context)

@login_required
def add_view(request):
    return render(request, 'add_trip.html')

@login_required
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

@login_required
def join_trip(request, trip_id):
    user = Users.objects.get(id = int(request.session['user']['id']))
    user.trips.add(Trips.objects.get(id = trip_id))
    return redirect(request.META.get('HTTP_REFERER'))