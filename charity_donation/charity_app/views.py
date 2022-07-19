from django.db.models.aggregates import Sum
from django.shortcuts import render
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


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        pass



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
