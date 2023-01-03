from django.shortcuts import render, redirect
from .models import Location, UserLocations
from users.models import Student
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from . import maps


def add_location(request):
    if request.user.is_authenticated:
        context = {}
        if request.method == 'POST':
            location_name = request.POST['Name']
            street_address = request.POST['Address']
            address = f'{street_address}'
            student = Student.objects.get(stud=request.user)
            try:
                lat, lng = maps.get_long_lat(address)
            except LookupError:
                messages.info(request, 'failed to find location on map')
                return redirect('dashboard', pk=student.id)
            location = UserLocations.objects.create(
                user=student,
                location_name=location_name,
                lat=lat,
                long=lng,
                street_address=street_address,
            )
            location.save()
            messages.info(request, 'Location Added')
            return redirect('dashboard', pk=student.id)
        else:
            return render(request, 'add_location.html', context)
    else:
        messages.info(request, 'Login to add personal location')
        return redirect('login')


def update_location(request):
    if request.user.is_authenticated:
        context = {}
        if request.method == 'POST':
            street_address = request.POST['Address']
            address = f'{street_address}'
            student = Student.objects.get(stud=request.user)
            try:
                lat, lng = maps.get_long_lat(address)
            except LookupError:
                messages.info(request, 'failed to find location on map')
                return redirect('dashboard', pk=student.id)
            student.street_address = address
            student.city = ''
            student.state = ''
            student.lat = lat
            student.long = lng
            student.save()
            messages.info(request, 'Location Updated')
            return redirect('dashboard', pk=student.id)
        else:
            return render(request, 'update_location.html', context)
    else:
        messages.info(request, 'Login to add personal location')
        return redirect('login')


def delete_location(request, pk):
    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        try:
            location = Location.objects.get(id=pk, student=student)
            location.delete()
            return redirect('dashboard', pk=student.id)
        except ObjectDoesNotExist:
            messages.info(request, 'No location found')
            return redirect('dashboard', pk=student.id)
    else:
        messages.info(request, 'Login to delete location')
        return redirect('login')


def view_map(request):
    locations = []
    main_locations = Location.objects.all()
    for location in main_locations:
        if location.has_lng_lat:
            item = {
                'lat': location.lat,
                'lng': location.long
            }
            locations.append(item)
        else:
            try:
                address = f'{location.street_address}, {location.city}. {location.state}'
                lat, lng = maps.get_long_lat(address)
                location.lat = lat
                location.long = lng
                location.has_lng_lat = True
                location.save()
                item = {
                    'lat': location.lat,
                    'lng': location.long
                }
                locations.append(item)
            except LookupError:
                pass
    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        student_locations = UserLocations.objects.filter(user=student)
        for location in student_locations:
            if location.has_lng_lat:
                item = {
                    'lat': location.lat,
                    'lng': location.long
                }
                locations.append(item)
            else:
                try:
                    address = f'{location.street_address}, {location.city}. {location.state}'
                    lat, lng = maps.get_long_lat(address)
                    location.lat = lat
                    location.long = lng
                    location.has_lng_lat = True
                    location.save()
                    item = {
                        'lat': location.lat,
                        'lng': location.long
                    }
                    locations.append(item)
                except LookupError:
                    pass
    context = {
        'locations': locations,
        'main_locations': main_locations
    }
    return render(request, 'loc_maps.html', context=context)


def get_direction(request):
    if request.method == 'POST':
        origin = request.POST['origin']
        destination = request.POST['destination']
        try:
            begin = Location.objects.get(location_name=origin)
        except ObjectDoesNotExist:
            begin = UserLocations.objects.get(location_name=origin)
        try:
            end = Location.objects.get(location_name=destination)
        except ObjectDoesNotExist:
            end = UserLocations.objects.get(location_name=destination)

        context = {
            'origin': {
                'lat': begin.lat,
                'lng': begin.long
            },
            'destination': {
                'lat': end.lat,
                'lng': end.long
            }
        }
        return render(request, 'directions.html', context)
# Create your views here.
