from email.headerregistry import ContentDispositionHeader
from django.shortcuts import render
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, user!")


def view_logs(request):
    context = {
        "sample_log_list": ["You logged in at 1:00pm", "You added a new course", "You logged out at 3:00pm"],
    }
    return render(request, "schedule/logs.html", context)

def home_page(request):
    time_duration = [
        "9:00AM", "10:00AM", "11:00AM", "12:00PM", "1:00PM", 
        "2:00PM", "3:00PM", "4:00PM", "5:00PM", 
        "6:00PM", "7:00PM"
    ]
    
    context = {
        "user_name": "", 
        "last_login": "", 
        "login_time": "", 
        "time_period": time_duration}
    return render(request, "schedule/home.html", context)