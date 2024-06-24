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
            upload_dir = os.path.join(settings.BASE_DIR, 'upload') 
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            f=request.FILES['file']
            file_path = os.path.join(upload_dir, f.name) 
            print(file_path)
            with open(file_path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk) 
            messages.success(request,"File uploaded successfuly") 
            return redirect('/upload')
    return render(request,'upload.html',{'form':excelForm}) 

@login_required(login_url='/')
def querybuilder(request):
    if request.method == 'POST': 
        filters = {}
        company_name = request.POST.get('Companyname')
        domain = request.POST.get('Domain')
        year_founded = request.POST.get('Yearfounded')
        country = request.POST.get('Country')
        current_employees = request.POST.get('Currenteployees')
        total_employees = request.POST.get('Totalemployees')
        if company_name:
            filters['name'] = company_name
        if domain:
            filters['domain'] = domain
        if year_founded:
            filters['year founded'] = year_founded
        if country:
            filters['country'] = country
        if current_employees:
            filters['current employee estimate'] = current_employees
        if total_employees:
            filters['total employee estimate'] = total_employees
        upload_dir = os.path.join(settings.BASE_DIR, 'upload')
        exceldata=[]
        for f in os.listdir(upload_dir):
            exceldata.append(pd.read_csv(os.path.join(upload_dir, f) ))

        if not exceldata:
            return HttpResponse("No data found")

        df = pd.concat(exceldata, ignore_index=True)
        print(df)

        # Apply filters to the DataFrame
        for column, value in filters.items():
            df = df[df[column].astype(str).str.contains(str(value), case=False, na=False)]

        row_count = df.shape[0]
        print("Filtered row count:", row_count)
        messages.success(request,str(row_count)+' records found for the query')
        return redirect('/querybuilder')
        # except Exception as e:
        #     return redirect('/querybuilder')
    return render(request,'querybuilder.html') 

@login_required(login_url='/')
def insert(request):
    try:
        password=request.POST.get('password')
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
    

