from django.shortcuts import render, redirect
from authentication.models import *

def index(request):
    data = CustomUser.objects.all()
    return render(request, 'home/index.html', {"all_data":data})