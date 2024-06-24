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
