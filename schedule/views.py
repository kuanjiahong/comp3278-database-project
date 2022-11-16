from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from smtplib import SMTPException
from datetime import datetime, date, timedelta
from schedule.models import  Class, Enrolment, Course, Teaching
from users.models import User
import pytz
import math
from datetime import datetime
from django.http import JsonResponse

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
    courses_enrolled = Course.objects.filter(students = request.user)
    classes = Class.objects.filter(course__in = courses_enrolled).order_by('class_day')

    upcoming_classes = retrieve_upcoming_classes(request.user.id)

    time_duration = [
        "9:30AM","10:00AM", "10:30AM","11:00AM", "11:30AM","12:00PM", "12:30PM","1:00PM", "1:30PM",
        "2:00PM", "2:30PM","3:00PM", "3:30PM","4:00PM", "4:30PM","5:00PM", "5:30PM", 
        "6:00PM", "6:30PM", "7:00PM", "7:30PM", "8:00PM", "8:30PM", "9:00PM", "9:30PM", "10:00PM" 
    ]
    time_formatted = [datetime.strptime(time,"%I:%M%p").time() for time in time_duration]
    
    # fetch classes into dictionary
    lectures = [
        {
            "Code": class_ed.course.code,
            "Name": class_ed.course.name,
            "Weekday": class_ed.class_day,
            "Rowspan": 0,
            "Start_time": class_ed.start_time,
            "End_time": class_ed.end_time,
            "Location": class_ed.location,
            "Type": class_ed.class_type,
            "Moodle_link": class_ed.course.moodle_link
        } for class_ed in classes
    ]
    # calculate rowspan for each class
    for class_ed in lectures:
        dt = datetime.now()
        temp_start = datetime.combine(dt, class_ed["Start_time"])
        temp_end = datetime.combine(dt, class_ed["End_time"])
        hour = temp_end - temp_start
        class_ed["Rowspan"] = math.ceil(hour.total_seconds() / 1800)
    timetablestr = ""
    # dictionary to hold weekday that should be skipped from printing td
    weekday = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    class_type ={"L": "Lecture", "T": "Tutorial"}
    for time in time_formatted:
        timetablestr += "<tr>"
        timetablestr += f"<th scope=\"row\">{time.strftime('%I:%M%p')}</th>"
        # a week can only skip a single weekday
        skipchance = {"1": 1, "2": 1, "3": 1, "4": 1,"5": 1}
        # hold skipped days
        skipped = 0
        for days in range(1, 6):
            # flag for searching classes
            found = 0
            for lecture in lectures:
                if lecture["Start_time"] == time and lecture["Weekday"] == str(days): # class found
                    weekday[lecture["Weekday"]] += lecture["Rowspan"]
                    timetablestr += f"<td rowspan=\"{lecture['Rowspan']}\">"
                    timetablestr += f"<div class = \"box\"><span><a href='{lecture['Moodle_link']}'><b>{lecture['Code']}</b></a>"
                    timetablestr += f"<br >{lecture['Name']}<br />"
                    timetablestr += f"{lecture['Start_time'].strftime('%I:%M %p')} - {lecture['End_time'].strftime('%I:%M %p')}<br />"
                    timetablestr += f"{lecture['Location']}<br />"
                    timetablestr += f"{class_type[lecture['Type']]}</span></div></td>"
                    found = 1
                    break
            if found == 0:
                if weekday[str(days)] > 0 and skipchance[str(days)]: # skip the td 
                    weekday[str(days)] -= 1
                    skipped += 1
                    continue
                else:
                    timetablestr += "<td></td>"
          
        for i in range(skipped): # add the skipped td back into the row
            timetablestr += "<td></td>"

                
        timetablestr += "</tr>"

    context = {
        "last_login": request.user.last_login.astimezone(pytz.timezone("Asia/Hong_Kong")).strftime("%d/%m/%Y %I:%M %p"),
        "time_formatted": time_formatted,
        # "classes": lectures,
        "timetablestr":timetablestr,
        "upcoming_classes": upcoming_classes,
    }
    
    return render(request, "schedule/home.html", context)

@login_required
def send_upcoming_classes(request):
    # retrieve upcoming classes
    upcoming_classes = retrieve_upcoming_classes(request.user.id)
    
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
        message += f"Lecturers: {upcoming_class['lecturers']}\n"
        message += f"Tutors: {upcoming_class['tutors']}\n"
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

def retrieve_upcoming_classes(user_id):
    result = []
    try:
        # Retrieve all user's enrolment
        user_all_enrolment = Enrolment.objects.filter(student=user_id)

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

                    if difference_in_time.days <= -1:
                        continue
                    elif difference_in_time.seconds <= 3600: # 1 hour = 3600 seconds
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