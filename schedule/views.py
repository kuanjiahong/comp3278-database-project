from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
from django.http import HttpResponse
from smtplib import SMTPException
from datetime import datetime, date, timedelta
from schedule.models import  Class, Enrolment, Course, Teaching
from users.models import User
import pytz
import math
from datetime import datetime

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
            try:
                validate_email(email)
            except ValidationError:
                user = None
            else:
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
    # print the detailed log when users log out
    email = request.user.email
    # take last login time from the user's record
    last_login = request.user.last_login.astimezone(pytz.timezone("Asia/Hong_Kong"))
    
    # find the user's IP address from the request body
    remote_addr = request.META['REMOTE_ADDR']

    # take the current time
    time_now = datetime.now().astimezone(pytz.timezone("Asia/Hong_Kong"))
    
    # calculate the current duration since the user logged in
    duration = (time_now - last_login).total_seconds()

    # prepare the log list and render the page
    log_list = [
        {
            "content": f"{email} logged in from {remote_addr}",
            "timestamp": last_login.strftime('%d/%m/%Y %I:%M:%S %p')
        },
        {
            "content": f"{email} has been logged in for {duration:.2f} seconds",
            "timestamp": time_now.strftime('%d/%m/%Y %I:%M:%S %p')
        }
    ]
    context = {
        "log_list": log_list
    }
    logout(request)
    return render(request, "schedule/logout.html", context)

@login_required
def view_logs(request):
    email = request.user.email
    # take last login time from the user's record
    last_login = request.user.last_login.astimezone(pytz.timezone("Asia/Hong_Kong"))
    
    # find the user's IP address from the request body
    remote_addr = request.META['REMOTE_ADDR']

    # take the current time
    time_now = datetime.now().astimezone(pytz.timezone("Asia/Hong_Kong"))
    
    # calculate the current duration since the user logged in
    duration = (time_now - last_login).total_seconds()

    # prepare the log list and render the page
    log_list = [
        {
            "content": f"{email} logged in from {remote_addr}",
            "timestamp": last_login.strftime('%d/%m/%Y %I:%M:%S %p')
        },
        {
            "content": f"{email} has been logged in for {duration:.2f} seconds",
            "timestamp": time_now.strftime('%d/%m/%Y %I:%M:%S %p')
        }
    ]
    context = {
        "log_list": log_list
    }
    return render(request, "schedule/logs.html", context)

@login_required
def home_page(request):
   # get enrolled courses of user and its corresponding classes
    courses_enrolled = Course.objects.filter(students=request.user, offered=True)
    classes = Class.objects.filter(course__in=courses_enrolled).order_by('class_day')
   

    time_duration = [
        "9:30AM","10:00AM", "10:30AM","11:00AM", "11:30AM","12:00PM", "12:30PM","1:00PM", "1:30PM",
        "2:00PM", "2:30PM","3:00PM", "3:30PM","4:00PM", "4:30PM","5:00PM", "5:30PM", 
        "6:00PM", "6:30PM", "7:00PM", "7:30PM", "8:00PM", "8:30PM", "9:00PM", "9:30PM", "10:00PM" 
    ]
    time_formatted = [datetime.strptime(time,"%I:%M%p").time() for time in time_duration]
    
    # fetch classes into dictionary
    lectures = [
        {
            "code": class_ed.course.code,
            "name": class_ed.course.name,
            "weekday": class_ed.class_day,
            "row_span": 0,
            "start_time": class_ed.start_time,
            "end_time": class_ed.end_time,
            "location": class_ed.location,
            "type": class_ed.class_type,
            "moodle_link": class_ed.course.moodle_link
        } for class_ed in classes
    ]
  

    # calculate rowspan for each class
    for class_ed in lectures:
        dt = datetime.now()
        temp_start = datetime.combine(dt, class_ed["start_time"])
        temp_end = datetime.combine(dt, class_ed["end_time"])
        hour = temp_end - temp_start
        class_ed["row_span"] = math.ceil(hour.total_seconds() / 1800)
    timetablestr = ""
    
    # dictionary to hold how many next rows to skip at each weekday column
    weekday_skip_next_rows = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    
    class_type ={"L": "Lecture", "T": "Tutorial"}
    for time in time_formatted:
        timetablestr += "<tr>"
        timetablestr += f"<th scope=\"row\">{time.strftime('%I:%M%p')}</th>"

        for days in range(1, 6):
            # flag for searching classes
            found = 0
            for lecture in lectures:
                if lecture["start_time"] == time and lecture["weekday"] == str(days): # class found
                    # skip the next (lecture's rowspan - 1) rows in the lecture's weekday column
                    weekday_skip_next_rows[lecture["weekday"]] += lecture["row_span"] - 1

                    # add the lecture entry to the timetable
                    timetablestr += f"<td rowspan=\"{lecture['row_span']}\">"
                    timetablestr += f"<div class = \"box\"><span><a href='{lecture['moodle_link']}'><b>{lecture['code']}</b></a>"
                    timetablestr += f"<br >{lecture['name']}<br />"
                    timetablestr += f"{lecture['start_time'].strftime('%I:%M %p')} - {lecture['end_time'].strftime('%I:%M %p')}<br />"
                    timetablestr += f"{lecture['location']}<br />"
                    timetablestr += f"{class_type[lecture['type']]}<br />"
                    timetablestr += f"</span></div></td>"
                    found = 1
                    break
            
            # if no class is found
            if found == 0:
                # check if the weekday row is to skip
                if weekday_skip_next_rows[str(days)] > 0:
                    # subtract one row as it is skipped
                    weekday_skip_next_rows[str(days)] -= 1
                    continue

                # otherwise print an empty weekday row
                else:
                    timetablestr += "<td></td>"

        # close a row i.e. a time period
        timetablestr += "</tr>"


    upcoming_classes = retrieve_upcoming_classes(request)

    context = {
        "last_login": request.user.last_login.astimezone(pytz.timezone("Asia/Hong_Kong")).strftime("%d/%m/%Y %I:%M %p"),
        "time_formatted": time_formatted,
        "timetablestr":timetablestr,
        "upcoming_classes": upcoming_classes,
    }
    
    return render(request, "schedule/home.html", context)

@login_required
def send_upcoming_classes(request):
    # retrieve upcoming classes
    upcoming_classes = retrieve_upcoming_classes(request)
    
    # do nothing if there is no upcoming class
    if len(upcoming_classes) == 0:
        return HttpResponse(content="No upcoming class.")

    # otherwise, prepare the email
    subject = "[COMP3278 HKU ICMS] You have class in ONE hour!"
    message = ""
    for upcoming_class in upcoming_classes:
        message += f"The class {upcoming_class['code']} {upcoming_class['name']} is starting soon.\n"
        message += f"Location: {upcoming_class['location']}\n"
        message += f"Time: {upcoming_class['start_time']} - {upcoming_class['end_time']}\n"
        message += f"Lecturer(s): {upcoming_class['lecturers']}\n"
        message += f"Tutor(s): {upcoming_class['tutors']}\n"
        if upcoming_class['teacher_message'] != "":
            message += f"Teacher's message: {upcoming_class['teacher_message']}\n"
        if upcoming_class['zoom_link'] != "":
            message += f"Zoom link: {upcoming_class['zoom_link']}\n"
        message += f"Course material: {upcoming_class['course_material']}\n\n"
    message += "Please DO NOT reply to this email.\n\n"
    message += "Regards,\nCOMP3278 HKU ICMS"
    
    # send the email
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[User.objects.get(pk=request.user.id).email]
        )
    except SMTPException:
        return HttpResponse(content="FAILED to send email")

    return HttpResponse(content="Email sent SUCCESSFULLY.")

@login_required
def retrieve_upcoming_classes(request):
    result = []
    try:
        # Retrieve all user's enrolment
        user_all_enrolment = Enrolment.objects.filter(student=request.user, course__offered=True)
        # Get the course in each enrolment record
        for enrolment in user_all_enrolment:
            user_registerd_course = Course.objects.get(pk=enrolment.course.id)
            all_staff_records = Teaching.objects.filter(course=user_registerd_course.id)
            tutors = []
            lecturers = []
            for teach in all_staff_records:
                if teach.role == "T":
                    tutors.append(teach.staff.name)
                elif teach.role == "L":
                    lecturers.append(teach.staff.name)
            
            tutors = ", ".join(tutors)
            lecturers = ", ".join(lecturers)

            classes = Class.objects.filter(course=user_registerd_course.id) # Retrieve all classess for this course
            
            # Check if any of the classess is starting in less than one hour
            for a_class in classes:
                today_weekday = date.today().isoweekday() # mon: 1 ... sun: 7
                the_class_day = int(a_class.class_day) # mon: 1 ... sun: 7
                if today_weekday == the_class_day:
                    current_time = timedelta(hours=datetime.now().time().hour, minutes=datetime.now().time().minute)
                    the_class_time = timedelta(hours=a_class.start_time.hour, minutes=a_class.start_time.minute)
                    difference_in_time = the_class_time - current_time

                    if difference_in_time.total_seconds() <= 3600 and difference_in_time.total_seconds() > 0: # 1 hour = 3600 seconds
                        temp = {
                            "code": user_registerd_course.code,
                            "name": user_registerd_course.name,
                            "lecturers": lecturers,
                            "tutors": tutors,
                            "location": a_class.location,
                            "start_time": a_class.start_time.strftime("%I:%M %p"),
                            "end_time": a_class.end_time.strftime("%I:%M %p"),
                            "teacher_message": a_class.teacher_message,
                            "zoom_link": a_class.zoom_link,
                            "course_material": user_registerd_course.moodle_link,
                        }
                        result.append(temp)
                else:
                    continue
        
        # After iterating all the enrolment record, return the array of upcoming classess
        return result
    except ObjectDoesNotExist:
        print("One of the object does not exist")
        return None
    except MultipleObjectsReturned:
        print("More than one objects were retrieved")
        return None