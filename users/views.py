from django.shortcuts import render, redirect
from .models import Student
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView
from maps.models import Location, UserLocations
from maps import maps


def register_view(request):
    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        return redirect('dashboard', pk=student.id)

    if request.method == 'POST':
        try:
            User.objects.get(username=request.POST['mat_number'])
            messages.info(request, 'MatNo already exist, please log in')
            return redirect('login.html')
        except ObjectDoesNotExist:
            username = request.POST['mat_number']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            street_address = request.POST['street_address']
            city = request.POST['city']
            state = request.POST['state']
            password = request.POST['password']
            password2 = request.POST['password2']
            if password == password2:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = firstname
                user.last_name = lastname
                user.save()
                student = Student.objects.create(
                    stud=user,
                    mat_no=username,
                    street_address=street_address,
                    city=city,
                    state=state,
                    slug=user.username
                )
                student.save()
                user = authenticate(request, username=username, password=password)
                login(request, user)
                messages.info(request, "Verification Successful")
                student = Student.objects.get(stud=request.user)
                return redirect('dashboard', pk=student.id)
            else:
                messages.error(request, 'Password does not match')
                return render(request, 'register.html')
    else:
        return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        return redirect('dashboard', pk=student.id)
    if request.method == 'POST':
        username = request.POST['mat_number']
        password = request.POST["password"]
        check_user = User.objects.filter(username=username).exists()
        if check_user is False:
            messages.info(request, "MatNo not registered")
            return redirect('login')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, "Successfully logged in.")
            student = Student.objects.get(stud=user)
            return redirect('dashboard', pk=student.id)
        else:
            messages.info(request, 'invalid login details')
            return redirect('login')
    else:
        messages.info(request, 'hello')
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


class Dashboard(DetailView):

    model = Student
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        student = Student.objects.get(stud=self.request.user)
        locations = Location.objects.all()
        user_locations = UserLocations.objects.filter(user=student)
        context['locations'] = locations
        context['user_locations'] = user_locations
        return context


def view_location(request, pk, whose):
    match whose:
        case 'General':
            try:
                location = Location.objects.get(id=pk)
                if location.has_lng_lat:
                    context = {
                        'location': location
                    }
                    return render(request, 'maps.html', context)
                else:
                    try:
                        address = f'{location.street_address}, {location.city}. {location.state}'
                        lat, lng = maps.get_long_lat(address)
                        location.lat = lat
                        location.long = lng
                        location.has_lng_lat = True
                        location.save()
                        context = {
                            'location': location
                        }
                        return render(request, 'maps.html', context)
                    except LookupError:
                        messages.info(request, 'location unavailable')
                        return redirect('map')
            except ObjectDoesNotExist:
                messages.info(request, 'location unavailable')
                return redirect('map')
        case 'User':
            if request.user.is_authenticated:
                student = Student.objects.get(stud=request.user)
                try:
                    location = UserLocations.objects.get(id=pk, user=student)
                    if location.has_lng_lat:
                        context = {
                            'location': location
                        }
                        return render(request, 'maps.html', context)
                    else:
                        try:
                            address = f'{location.street_address}, {location.city}. {location.state}'
                            lat, lng = maps.get_long_lat(address)
                            location.lat = lat
                            location.long = lng
                            location.has_lng_lat = True
                            location.save()
                            context = {
                                'location': location
                            }
                            return render(request, 'maps.html', context)
                        except LookupError:
                            messages.info(request, 'location unavailable')
                            return redirect('map')
                except ObjectDoesNotExist:
                    messages.info(request, 'location unavailable')
                    return redirect('map')
            else:
                return redirect('map')
        case _:
            messages.info(request, 'location unavailable')
            return redirect('map')


# Create your views here.
