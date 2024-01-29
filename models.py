from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def getFileName(request,Filename):
    now_time=datetime.datetime.now().strtime("%y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path('uploads/',)


class CustomUser(User):
    
    
 
    
        
    """
    Your model definition goes here.
    """

"""
class PredictedDetaild.join(models.Model):
    name=models.CharField(max_length=20,null=False, blank=False)
    image=models.ImageField(upload_to=getFileName null=True,blank=True)
    email=models.CharField(max_length=50,null=False, blank=False)
    date=models.DateTimeField(auto_now_add=true)
    
    
class Datas(models.Model):
    Name=models.CharField(max_length=20,default="")
    Email=models.CharField(max_length=20,default="")
    Password=models.CharField(max_length=20,default="")
    RePassword=models.CharField(max_length=20,default="") 
 """