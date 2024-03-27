import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Tab(models.Model):
    name = models.CharField(max_length=200)
    notation = models.CharField(max_length=5)
    key = models.CharField(max_length=3)
    time = models.CharField(max_length=3)
    notes = models.CharField(max_length=15000)
    notelist = models.JSONField()
    tablature = models.CharField(max_length=5)
    clef = models.CharField(max_length=10)
    tuning = models.CharField(max_length=8)
    tab_stems = models.CharField(max_length=5)
    tab_stems_direction = models.CharField(max_length=2)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=20,blank=True, null=True)
    level = models.CharField(max_length=20,blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "profile")
    securityQuestion1 = models.CharField(max_length=100)
    securityAnswer1 = models.CharField(max_length=100)
    securityQuestion2 = models.CharField(max_length=100)
    securityAnswer2 = models.CharField(max_length=100)
    securityQuestion3 = models.CharField(max_length=100)
    securityAnswer3 = models.CharField(max_length=100)
    genre1 = models.CharField(max_length=20,blank=True, null=True)
    genre2 = models.CharField(max_length=20,blank=True,  null=True)
    genre3 = models.CharField(max_length=20,blank=True,  null=True)
    experienceLevel = models.CharField(max_length=30, default='Intermediate')

class Favourite(models.Model):
    user =  models.OneToOneField(User, on_delete = models.CASCADE, related_name = "favourite")
    tabId = models.ForeignKey(Tab, on_delete=models.CASCADE)