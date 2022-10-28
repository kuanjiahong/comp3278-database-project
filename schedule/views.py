from email.headerregistry import ContentDispositionHeader
from genericpath import exists
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

def login_mainpage(request):
    if request.POST:
        print(f"Email: {request.POST['email']}")
        print(f"Password: {request.POST['password']}")
        
        if 'face_auth' in request.FILES:
            with open('face_auth/face_auth_temp.mp4', "wb+") as destination:
                for chunk in request.FILES['face_auth'].chunks():
                    destination.write(chunk)
        context = {"error": "Incorrect email or password"}
        return render(request, 'schedule/login.html', context=context)
    return render(request, 'schedule/login.html')

def view_logs(request):
    context = {
        "sample_log_list": ["None", "None", "None"],
    }
    return render(request, "schedule/logs.html", context)

def home_page(request):
    time_duration = [
        "9:00AM", "9:30AM","10:00AM", "10:30AM","11:00AM", "11:30AM","12:00PM", "12:30PM","1:00PM", "1:30PM",
        "2:00PM", "2:30PM","3:00PM", "3:30PM","4:00PM", "4:30PM","5:00PM", "5:30PM", 
        "6:00PM", "6:30PM","7:00PM", "7:30PM"
    ]

    context = {
        "user_name": "", 
        "last_login": "", 
        "login_time": "", 
        "time_period": time_duration
        }
    
    return render(request, "schedule/home.html", context)