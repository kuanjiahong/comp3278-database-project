from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pytz

def login_mainpage(request):
    # redirect to home if the user has logged in already
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
        
        # log user in and redirect to home if authentication passed
        login(request, user)
        return redirect("/schedule/home")

    return render(request, 'schedule/login.html')

@login_required
def logout_mainpage(request):
    logout(request)
    return redirect("/schedule/login")


@login_required
def view_logs(request):
    email = request.user.email
    last_login = request.user.last_login.astimezone(pytz.timezone("Asia/Hong_Kong")).strftime("%I:%M %p")
    remote_addr = request.META['REMOTE_ADDR']
    context = {
        "log_list": [f"{email} logged in at {last_login} from {remote_addr}"],
    }
    return render(request, "schedule/logs.html", context)

@login_required
def home_page(request):
    """
    TODO:
        make a query to find user's weekly schedule
        check if the user has a class within an hour
        if so, provide details of the upcoming class and display the full schedule
        otherwise, display the full schedule
    """
    time_duration = [
        "9:00AM", "9:30AM","10:00AM", "10:30AM","11:00AM", "11:30AM","12:00PM", "12:30PM","1:00PM", "1:30PM",
        "2:00PM", "2:30PM","3:00PM", "3:30PM","4:00PM", "4:30PM","5:00PM", "5:30PM", 
        "6:00PM", "6:30PM","7:00PM", "7:30PM"
    ]
    
    context = {
        "last_login": request.user.last_login.astimezone(pytz.timezone("Asia/Hong_Kong")).strftime("%d/%m/%Y %I:%M %p"),
        "time_period": time_duration
        # TODO: add details of the upcoming class (if any) and the full schedule here
    }
    
    return render(request, "schedule/home.html", context)