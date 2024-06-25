from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CoreUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    loginflag=models.BooleanField(default=False)

    @staticmethod
    def login_user(request,user,coreuser):
        if user:
            request.session['adid']=user.username
            request.session['loginflag']=coreuser.loginflag
            request.session['user_id']=coreuser.user_id

    class Meta:
        db_table='coreuser'

class ExcelData(models.Model):
    name=models.CharField(max_length=300)
    domain=models.CharField(max_length=300)
    yearfounded=models.CharField(max_length=10)
    industry=models.CharField(max_length=100)
    sizerange=models.CharField(max_length=100)
    locality=models.CharField(max_length=100)
    country=models.CharField(max_length=100)	
    linkedinurl=models.CharField(max_length=300)
    currentemployeeestimate=models.CharField(max_length=300)
    totalemployeeestimate=models.CharField(max_length=300)

    class Meta:
        db_table='exceldata'