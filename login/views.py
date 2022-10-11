from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def login_mainpage(request):
    return render(request,'index.html')