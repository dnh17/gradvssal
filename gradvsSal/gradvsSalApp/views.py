from django.shortcuts import render

# Create your views here.


from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import *

def HomeView(request):
    template_name = 'HealthNetApp/login.html'