from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.core.exceptions import ObjectDoesNotExist



from .models import *

def HomeView(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    template_name = 'home.html'
    return render(request, template_name)