from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import Donation, Institution


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')


class TestView(View):

    def get(self, request):
        return render(request, 'base.html')


class AddDonationView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'index'

    def get(self, request):
        user = User.objects.all()

        return render(request, 'form.html', {'user': user})


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('Błędny login lub hasło')


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        if request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('email') and \
                request.POST.get('password') and request.POST.get('password2'):
            user = User()
            user.username = request.POST['email']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.set_password(request.POST['password'])
            user.save()
            return render(request, 'login.html')

        else:
            return render(request, 'register.html')


class IndexView(View):

    def get(self, request):
        donation_counter = Donation.objects.aggregate(TOTAL=Sum('quantity'))['TOTAL']
        institution_counter = Donation.objects.values('institution').distinct().count()
        institution = Institution.objects.all()

        ctx = {'donation_counter': donation_counter,
               'institution_counter': institution_counter,
               'institution': institution,
               }
        return render(request, 'index.html', ctx)


class ProfileView(View):

    def get(self, request):
        user = User.objects.all()

        return render(request, 'profile.html', {'user': user})
