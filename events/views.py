from django.shortcuts import render, redirect, get_object_or_404
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect, Http404
from .models import Events, Venue
from .forms import VenueForm, EventsForm


# Delete of Venue an Event
def delete_venue(request, venue_id):
    try:
        venue = Venue.objects.get(pk=venue_id)
        venue.delete()
        return redirect('list_venues')
    except Events.DoesNotExist:
        raise Http404("Event does not exist")


# Delete of views an Event
def delete_event(request, event_id):
    try:
        event = Events.objects.get(pk=event_id)
        event.delete()
        return redirect('list-events')
    except Events.DoesNotExist:
        raise Http404("Event does not exist")


def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventsForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html',{'form': form,
                                                    ' submitted': submitted})


def update_event(request, event_id):
    event = Events.objects.get(pk=event_id)
    form = EventsForm(request.POST or None, instance= event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request,'events/update_event.html',
                  {'event':event,
                   'form':form})


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance= venue)
    if form.is_valid():
        form.save()
        return redirect('list_venues')
    return render(request,'events/update_venue.html',
                  {'venue':venue,
                   'form':form})



def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request,'events/search_venues.html',
                      {'searched': searched,
                       'venues':venues,})
    else:
        return render(request,'events/search_venues.html',
                      {'searched': searched,
                       'venues':venues,})


    

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request,'events/show_venue.html',{'venue':venue,})



def list_venues(request):
    venue_list = Venue.objects.all()
    return render(request,'events/venue.html',{'venue_list':venue_list,})

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html',{'form': form,
                                                    ' submitted': submitted})



def all_events(request):
    event_list = Events.objects.all()
    return render(request, 'events/events_list.html',
                  {
                     'event_list': event_list ,
                  })


def home(request, year=datetime.now().year, month= datetime.now().strftime('%B')):
    name = "Olivier"
    month = month.capitalize()
    #convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    #create a calendar
    cal = HTMLCalendar().formatmonth(year,month_number)

    #Get current year
    now = datetime.now()
    current_year = now.year

    #Get current time
    time = now.strftime('%I:%M:%p')

    return render (request,
                   'events/home.html',{
                       "name": name,
                       "year": year,
                       "month": month,
                       "month_number": month_number,
                       "cal": cal,
                       "current_year": current_year,
                       "time": time,
                   })