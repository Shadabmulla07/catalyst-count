from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from home.models import CoreUser,ExcelData
from home.forms import excelForm
from django.contrib.auth.hashers import make_password
import pandas as pd
from django.conf import settings
import os
# Create your views here.
def mylogin(request):
    if request.method=='POST':
        username=request.POST.get('login')
        password=request.POST.get('password')
        print(username,password)
        user=authenticate(username=username,password=password)
        if not user:
            messages.warning(request,"Incorrect password")
            return redirect("/")
        else:
            login(request,user)
            coreuser=CoreUser.objects.get(user_id=user.id)
            CoreUser.login_user(request,user,coreuser)
            return redirect("upload/")
    return render(request,'login.html')

@login_required(login_url='/')
def mylogout(request):
    try:
        user=request.session['user_id']
        logout(request)
        if user in request.session:
            request.session.clear()
        coreuser=CoreUser.objects.get(user_id=user,loginflag=1)
        coreuser.loginflag=0
        coreuser.save()
        return redirect('/')
    except:
        return redirect('/')

@login_required(login_url='/')
def upload(request):
    excelfile=''
    if request.method == 'POST':  
        student = excelForm(request.POST, request.FILES)  
        if student.is_valid(): 
            print("hiiiii")
            print(request.FILES['file'])
            upload_dir = os.path.join(settings.BASE_DIR, 'upload')  # Construct upload directory path
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)  # Create upload directory if it doesn't exist
            f=request.FILES['file']
            file_path = os.path.join(upload_dir, f.name)  # Construct full file path
            print(file_path)
            with open(file_path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk) 
            exceldata=pd.read_csv(file_path)
            values=exceldata.values.tolist()
            print(values)
            for i in values:
                print(i)
                ExcelData.objects.create(companyid=i[0],name=i[1],domain=i[2],yearfounded=i[3],industy=i[4],sizerange=i[5],locality=i[6],county=i[7],linkedinurl=i[8],currentemployee=i[9],totalemployee=i[10])
            messages.success(request,"File uploaded successfuly") 
            return redirect('/upload')
    return render(request,'upload.html',{'form':excelForm}) 

@login_required(login_url='/')
def querybuilder(request):
    if request.method == 'POST': 
        filters = {}
        company_name = request.POST.get('Companyname')
        print(company_name)
        domain = request.POST.get('Domain')
        year_founded = request.POST.get('Yearfounded')
        country = request.POST.get('Country')
        current_employees = request.POST.get('Currenteployees')
        total_employees = request.POST.get('Totalemployees')

        if company_name:
            filters['name__icontains'] = company_name
        if domain:
            filters['domain__icontains'] = domain
        if year_founded:
            filters['yearfounded'] = year_founded
        if country:
            filters['county__icontains'] = country
        if current_employees:
            filters['currentemployee'] = current_employees
        if total_employees:
            filters['totalemployee'] = total_employees
        # try:
        count = ExcelData.objects.filter(**filters).count()
        messages.success(request,str(count)+' records found for the query')
        return redirect('/querybuilder')
        # except Exception as e:
        #     return redirect('/querybuilder')
    return render(request,'querybuilder.html') 

@login_required(login_url='/')
def insert(request):
    try:
        password=request.POST.get('password')
        print(password)
        print(request.POST.get('username'))
        print(request.POST.get('firstname'))
        print(request.POST.get('lastname'))
        id=User.objects.create(username=request.POST.get('username'),first_name=request.POST.get('firstname'),last_name=request.POST.get('lastname'),password=make_password(password)).id
        print(id)
        CoreUser.objects.create(loginflag=True,user_id=id)
        messages.success(request,"New user created")
        return redirect("/users")
    except:
        messages.warning(request,"something wrong")
        return redirect ("/users")

@login_required(login_url='/')
def users(request):
    userdata=CoreUser.objects.all()
    userdata=CoreUser.objects.select_related('user').all()
    for user in userdata:
        print(user.loginflag)
    return render(request,'users.html',{'userdata':userdata}) 

@login_required(login_url='/')
def delete(request,id):
    userid=list(CoreUser.objects.filter(id=id).values('user_id'))
    userid=[user['user_id']for user in userid]
    CoreUser.objects.filter(id=id).delete()
    d=User.objects.filter(id__in=userid).delete()
    return redirect("/users")
    

