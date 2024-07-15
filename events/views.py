from django.shortcuts import render, redirect, get_object_or_404
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect, Http404
from .models import Events, Venue
from .forms import VenueForm, EventsForm, EventsFormAdmin
from django.http import HttpResponse
import csv
from django.contrib import messages
# Import PDF Staff
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Import Pagination Staff
from django.core.paginator import Paginator



# Generate a PDF File Venue List
def venue_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create Canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a Text Object
    textob = c.beginText()  # Add parentheses to call the function
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    # Add some lines of text
    #lines = [
     #   "This is line 1",
      #  "This is line 2",
      #  "This is line 3",
    #]

    # Designate The Model
    venues = Venue.objects.all()
    # Create Blank List
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append("=============================")
    # Loop
    for line in lines:
        textob.textLine(line)
    # Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venues.pdf')

# Generate CSV File Venue List
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # Create CSV Writer
    writer = csv.writer(response)
    # Designate The Model
    venues = Venue.objects.all()

    # Add column headings to the csv file
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone',  'Email'])

    # Loop through and output
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])
        # Add an empty row for separation
        writer.writerow([])  
    
    return response



# Generate Text File Venue List
def venue_text(request):
    response = HttpResponse(content='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    # Designate The Model
    venues = Venue.objects.all()
    # Create Blank List
    lines = []
    # Loop Thu and output
    for venue in venues:
        lines.append(f'{venue.name}\n {venue.address}\n {venue.phone}\n {venue.zip_code}\n {venue.phone}\n {venue.web}\n {venue.email_address}\n')
    #lines = ["This is line 1\n",
          #   "This is line 2\n",
           #  "This is line 3\n\n",
             #"Kiniboua Gnaly est Genial\n"]
    # Write To TextFile
    response.writelines(lines)
    return response

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
        if request.user == event.manager:
             event.delete()
             messages.success(request, ("Event Delted!!"))
             return redirect('list-events')
        else :
            messages.success(request, ("Your Are Not Authorized To Delete This Event!!"))
            return redirect('list-events')
    except Events.DoesNotExist:
        raise Http404("Event does not exist")


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventsFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventsForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user  # Logged in User
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # Just Going To The Page, Not Submitting
        if request.user.is_superuser:
            form = EventsFormAdmin()
        else:
            form = EventsForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


def update_event(request, event_id):
    event = Events.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventsFormAdmin(request.POST or None, instance= event)
    else:
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
    
    # Set up Pagination
    p = Paginator(venue_list, 2)  # Utilise la variable venue_list pour la pagination
    page_number = request.GET.get('page')  # Utilise .get() pour obtenir la valeur de 'page'
    venues = p.get_page(page_number)  # Récupère l'objet de la page

    return render(request, 'events/venue.html', {
        'venue_list': venue_list,  # Cette ligne peut être retirée si elle n'est pas nécessaire
        'venues': venues
    })

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id #Logged in User
            venue.save()
            #form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html',{'form': form,
                                                    ' submitted': submitted})



def all_events(request):
    event_list = Events.objects.all().order_by('event_date')
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
