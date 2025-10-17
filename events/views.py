from django.shortcuts import redirect, render, get_object_or_404
from events.models import Event
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Q
from events.forms import *
from django.contrib import messages 
from events.forms import EventReportForm
# Create your views here.

def list_events(request):

    search_query = request.GET.get("search", '')
    filter_type = request.GET.get('filter', 'all')

    events = Event.objects.all().order_by('-posted_on')

    if search_query:
        events = events.filter(
            title__icontains = search_query
        ) | events.filter(
            venue__icontains = search_query
        ) | events.filter(
            description__icontains = search_query
        ) | events.filter(
            user__first_name__icontains = search_query
        )
    
    if filter_type == "posted_by_student":
        events = events.filter(user__role = "Student")
    elif filter_type == "posted_by_alumni":
        events = events.filter(user__role ="Alumni")
    elif filter_type == "posted_by_staff":
        events = events.filter(user__role ="Staff")
    elif filter_type == "upcoming":
        events = events.filter(start_date__gte = date.today())
    elif filter_type == "ongoing":
        events = events.filter(
            Q(start_date__lte = date.today()) & Q(end_date__gt = date.today()) | 
            (Q(end_date__isnull = True) & Q(start_date = date.today()))
        )
    elif filter_type == "held":
        events = events.filter(
            Q(end_date__lt = date.today()) | ( Q(start_date__lt = date.today()) & Q(end_date__isnull = True) )
        )
    
    context = {
        "events": events,
        "filter_type": filter_type,
        "search_query": search_query
    }

    return render(request, "events/list_events.html", context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk = event_id)
    previous_url = request.META.get('HTTP_REFERER','events:list_events')
    return render(request, "events/event_detail.html", {"event": event, "previous_url": previous_url})


@login_required
def post_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, "Event has been posted successfully.")
            return redirect("dashboard:view_events")

        else:
            messages.error(request, "Kindly fix the error")
    else:
        form = EventForm()

    previous_url = request.META.get('HTTP_REFERER', 'events:list_events')
    return render(request, "events/event_form.html", {"form":form, "previous_url": previous_url})

@login_required
def edit_event(request, event_id):
    
    event = get_object_or_404(Event, pk = event_id, user = request.user)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event details has been updated.")
            return redirect("events:list_events")
        else:
            messages.error(request, "Kindly inputs the details correctly.")
    else:
        form = EventForm(instance=event)
    
    previous_url = request.META.get('HTTP_REFERER', 'events:list_events')

    return render(request, "events/event_form.html", {"form": form, "event":event, "previous_url": previous_url})

@login_required
def delete_event(request, event_id):
    if request.method == "POST":
        event = get_object_or_404(Event, pk = event_id, user = request.user)
        event.delete()
        messages.success(request, "Your event has been deleted.")
        previous_url = request.META.get("HTTP_REFERER", "events:list_events")
        return redirect(previous_url)
    

@login_required
def report_event(request, event_id):
    event = Event.objects.get(pk = event_id)
    if request.method == 'POST':
        form = EventReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit = False)
            report.event = event
            report.reported_by = request.user
            report.save()
            messages.success(request, "Your report has been reported successfully.")
            return redirect("events:list_events")
    else:
        form = EventReportForm()

    return render(request, "events/report_event.html", {"form": form})