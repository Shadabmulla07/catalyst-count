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
    companyid=models.IntegerField()
    name=models.CharField(max_length=200)
    domain=models.CharField(max_length=200)
    yearfounded=models.CharField(max_length=10)
    industy=models.CharField(max_length=200)
    sizerange=models.CharField(max_length=10)
    locality=models.CharField(max_length=200)
    county=models.CharField(max_length=200)
    linkedinurl=models.CharField(max_length=200)
    currentemployee=models.IntegerField()
    totalemployee=models.IntegerField()

    class Meta:
        db_table='exceldata'