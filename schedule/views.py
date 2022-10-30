from datetime import tzinfo
import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pytz

def login_mainpage(request):
    if request.user.is_authenticated:
        return redirect("/schedule/home")
    if request.POST:
        # if it's a face login
        if 'face_auth_mp4' in request.FILES or 'face_auth_webm' in request.FILES:
            user = authenticate(request=request)
            if user is None:
                context = {"error": "Face NOT recognized"}
                return render(request, 'schedule/login.html', context=context)
            
        # otherwise, it's a email-password login
        else:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request=request, username=email, password=password)
            if user is None:
                context = {"error": "Incorrect email or password"}
                return render(request, 'schedule/login.html', context=context)
        # log user in if authentication passed
        login(request, user)
        return redirect("/schedule/home")

    return render(request, 'schedule/login.html')

@login_required(login_url="/schedule/login")
def logout_mainpage(request):
    if request.method == "GET":
        logout(request)
        return redirect("/schedule/login")

@login_required(login_url="/schedule/login")
def view_logs(request):
    context = {
        "sample_log_list": ["None", "None", "None"],
    }
    return render(request, "schedule/logs.html", context)

@login_required(login_url="/schedule/login")
def home_page(request):
    time_duration = [
        "9:00AM", "9:30AM","10:00AM", "10:30AM","11:00AM", "11:30AM","12:00PM", "12:30PM","1:00PM", "1:30PM",
        "2:00PM", "2:30PM","3:00PM", "3:30PM","4:00PM", "4:30PM","5:00PM", "5:30PM", 
        "6:00PM", "6:30PM","7:00PM", "7:30PM"
    ]
    
    context = {
        "last_login": request.user.last_login.astimezone(pytz.timezone("Asia/Hong_Kong")).strftime("%d/%m/%Y %I:%M %p"),
        "time_period": time_duration
    }
    
    return render(request, "schedule/home.html", context)