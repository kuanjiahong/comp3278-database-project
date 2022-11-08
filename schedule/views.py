from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date, timedelta
import pytz
from .models import Class, Enrolment, Course

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
    upcoming_class = retrieve_upcoming_class(request.user.id)

    time_duration = [
        "9:00AM", "9:30AM","10:00AM", "10:30AM","11:00AM", "11:30AM","12:00PM", "12:30PM","1:00PM", "1:30PM",
        "2:00PM", "2:30PM","3:00PM", "3:30PM","4:00PM", "4:30PM","5:00PM", "5:30PM", 
        "6:00PM", "6:30PM","7:00PM", "7:30PM"
    ]
    
    context = {
        "last_login": request.user.last_login.astimezone(pytz.timezone("Asia/Hong_Kong")).strftime("%d/%m/%Y %I:%M %p"),
        "time_period": time_duration,
        "upcoming_class": upcoming_class,
        # TODO: add full schedule:
        "full_schedule": None,
    }
    
    return render(request, "schedule/home.html", context)

def retrieve_upcoming_class(user_id):
    try:
        # Retrieve the object needed
        user_enrolment = Enrolment.objects.get(student=user_id)
        the_course_object = Course.objects.get(pk=user_enrolment.course.id)
        the_class_object = Class.objects.get(pk=the_course_object.id)

        # Check the day
        today_weekday = date.today().weekday()
        the_class_day = Class.WeekDays.values.index(the_class_object.class_day)
        if today_weekday == the_class_day:

            # Check the time
            current_time = datetime.now().time()
            the_class_time = the_class_object.start_time
            print('current time:', current_time)
            print('the class time:', the_class_time)
            difference_in_time = timedelta(hours = the_class_time.hour, minutes=the_class_time.minute) - timedelta(hours=current_time.hour, minutes=current_time.minute)
            print(difference_in_time.seconds)
            if difference_in_time.days <= -1 :
                print("Class is already over or it is ongoing")
                return None
            elif difference_in_time.seconds <= 3600:
                print("Class is starting less than one hour")
                result = {
                    "code": the_course_object.code,
                    "name": the_course_object.name,
                    "location": the_class_object.location,
                    "teacher_message": the_class_object.teacher_message,
                    "zoom_link": the_class_object.zoom_link,
                    "course_material": the_course_object.moodle_link,
                }
            return result
        else:
            print("There is no upcoming class")
            return None
    except ObjectDoesNotExist:
        print("One of the object does not exist")
        return None