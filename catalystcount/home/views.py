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
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QueryBuilderSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
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
            chunk_size = 10000 #declare chunk size as per your server performance
            for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                records = [
                    ExcelData(
                        name=row['name'],
                        domain=row['domain'],
                        yearfounded=row['year founded'],
                        industry=row['industry'],
                        sizerange=row['size range'],
                        locality=row['locality'],
                        country=row['country'],
                        linkedinurl=row['linkedin url'],
                        currentemployeeestimate=row['current employee estimate'],
                        totalemployeeestimate=row['total employee estimate']
                    ) for _, row in chunk.iterrows()
                ]
                ExcelData.objects.bulk_create(records)
            messages.success(request,"File uploaded successfuly") 
            return redirect('/upload')
    return render(request,'upload.html',{'form':excelForm}) 

@csrf_exempt
def querybuilder_api(request):
    if request.method == 'POST':
        serializer = QueryBuilderSerializer(data=request.POST)
        if serializer.is_valid():
            filters = {}
            company_name = serializer.validated_data.get('Companyname')
            domain = serializer.validated_data.get('Domain')
            year_founded = serializer.validated_data.get('Yearfounded')
            country = serializer.validated_data.get('Country')
            current_employees = serializer.validated_data.get('Currenteployees')
            total_employees = serializer.validated_data.get('Totalemployees')

            if company_name:
                filters['name__icontains'] = company_name  # Adjust based on your model field names
            if domain:
                filters['domain__icontains'] = domain
            if year_founded:
                filters['year_founded'] = year_founded
            if country:
                filters['country__icontains'] = country
            if current_employees:
                filters['current_employee_estimate'] = current_employees
            if total_employees:
                filters['total_employee_estimate'] = total_employees

            try:
                filtered_data = ExcelData.objects.filter(**filters)
                row_count = filtered_data.count()
                print(row_count)
                return JsonResponse(row_count, safe=False)
                # return Response({'row_count': row_count, 'data': list(filtered_data.values())})
            except:
                return Response({'error': 'Unknown error'})

    return Response({'error': 'Only POST method is allowed'}, status=405)

@login_required(login_url='/')
def querybuilder(request):
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
    

