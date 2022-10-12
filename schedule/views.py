from django.shortcuts import render
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, user!")


def view_logs(request):
    context = {
        "sample_log_list": ["You logged in at 1:00pm", "You added a new course", "You logged out at 3:00pm"],
    }
    return render(request, "schedule/logs.html", context)