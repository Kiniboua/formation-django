from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address =models.CharField(max_length=300)
    zip_code = models.CharField('Zip_code',max_length=15)
    phone = models.CharField('Contact Phone', max_length=25, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)

    def __str__(self):
        return self.name
    
   
class MyClubUser(models.Model):
    frist_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.frist_name + ' ' +self.last_name

class Events(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField(_("Event Date"), auto_now=False, auto_now_add=False)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    #venue = models.CharField(max_length=120)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    descriptions = models.TextField(blank=True) 
    attendees = models.ManyToManyField(MyClubUser, blank=True,)


    def __str__(self) :
        return self.name
    
