from django.shortcuts import render, redirect
from authentication.models import *
from events.models import Event
def index(request):
    data = CustomUser.objects.filter(role ="Alumni")
    all_events = Event.objects.all()
    return render(request, 'home/index.html', {"all_data":data, "events":all_events})