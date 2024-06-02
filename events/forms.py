from django import forms 
from django.forms import ModelForm
from .models import Venue, Events



class EventsForm (ModelForm):
    class Meta:
        model = Events
        fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'descriptions')
       
        widgets = {
              'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Events name'}),
              'event_date':  forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event Date'}),
              'venue': forms.Select(attrs={'class':'form-select', 'placeholder':'Venue'}),
              'manager': forms.Select(attrs={'class':'form-select', 'placeholder':'Manager'}),
              'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Attendees'}),
              'descriptions': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descriptions'}),
        }
        labels = {
            'name': 'Event Name',
            'event_date': 'YYY-MM-DD ',
            'venue': 'venue',
            'manager': 'manager',
            'attendees': 'attendees',
            'descriptions': 'descriptions',
        }


#Create a Venue Forms
class VenueForm (ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address')
       
        widgets = {
              'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue name'}),
              'address':  forms.TextInput(attrs={'class':'form-control', 'placeholder': 'address'}),
              'zip_code': forms.TextInput(attrs={'class':'form-control', 'placeholder':'zip_code'}),
              'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'phone'}),
              'web': forms.TextInput(attrs={'class':'form-control', 'placeholder':'web'}),
              'email_address': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'email_address'}),
        }
        labels = {
            'name': 'Venue Name',
            'address': 'Address',
            'zip_code': 'Zip Code',
            'phone': 'Phone',
            'web': 'Website',
            'email_address': 'Email Address',
        }
