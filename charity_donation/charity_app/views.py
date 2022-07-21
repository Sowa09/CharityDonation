from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import Donation, Institution


class TestView(View):

    def get(self, request):
        return render(request, 'base.html')


class AddDonationView(View):

    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'form-confirmation.html')
        else:
            return redirect('register')


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        if request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('email') and \
                request.POST.get('password') and request.POST.get('password2'):
            user = User()
            user.username = request.POST.get('email')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.password = request.POST.get('password')
            user.password2 = request.POST.get('password2')
            if user.password == user.password2:
                user.save()
                return render(request, 'login.html')
            else:
                return HttpResponse('Proszę podać takie same hasła')
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
