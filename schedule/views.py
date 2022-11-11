from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datetime import datetime, date, timedelta
from schedule.models import  Class, Enrolment, Course
import pytz
import smtplib
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
    email = request.user.email
    last_login = request.user.last_login.astimezone(pytz.timezone("Asia/Hong_Kong"))
    remote_addr = request.META['REMOTE_ADDR']
    time_now = datetime.now().astimezone(pytz.timezone("Asia/Hong_Kong"))
    duration = (time_now - last_login).total_seconds()
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
    last_login = request.user.last_login.astimezone(pytz.timezone("Asia/Hong_Kong"))
    remote_addr = request.META['REMOTE_ADDR']
    time_now = datetime.now().astimezone(pytz.timezone("Asia/Hong_Kong"))
    duration = (time_now - last_login).total_seconds()
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
   
    Courses_enrolled = Course.objects.filter(students = request.user)
    Classes = Class.objects.filter(course__in = Courses_enrolled).order_by('class_day')
    print(Classes)
    #weekday_order = ["mon","tue","wed","thu","fri","sat","sun"]
  
    

    
    """
    TODO:
        make a query to find user's weekly schedule
        check if the user has a class within an hour
        if so, provide details of the upcoming class and display the full schedule
        otherwise, display the full schedule
    """
    upcoming_classes = retrieve_upcoming_classes(request.user.id)


    time_duration = [
        "9:00AM", "9:30AM","10:00AM", "10:30AM","11:00AM", "11:30AM","12:00PM", "12:30PM","1:00PM", "1:30PM",
        "2:00PM", "2:30PM","3:00PM", "3:30PM","4:00PM", "4:30PM","5:00PM", "5:30PM", 
        "6:00PM", "6:30PM"
    ]
    '''time_duration = [
        "9:30AM", "10:30AM", "11:30AM", "12:30PM", "1:30PM",
        "2:30PM", "3:30PM", "4:30PM", "5:30PM", 
        "6:30PM"
    ]'''
    time_formatted = [datetime.strptime(time,"%I:%M%p").time() for time in time_duration ]
    
    #[print(time) for time in time_formatted]




    # fetch classes into dictionary
    lectures = [{"Name":class_ed.course,"Weekday":class_ed.class_day,"Rowspan":0,"Start_time":class_ed.start_time,"End_time":class_ed.end_time,"Location":class_ed.location,"Type":class_ed.class_type} for class_ed in Classes]
    #calculate rowspan for each class
    for class_ed in lectures:
        dt = datetime.now()
        temp_start = datetime.combine(dt,class_ed["Start_time"])
        temp_end = datetime.combine(dt,class_ed["End_time"])
        hour = temp_end-temp_start
        #print(class_ed["Name"])
        class_ed["Rowspan"] = math.ceil(hour.total_seconds()/1800)
        #print(math.ceil(hour.total_seconds()/1800))
    timetablestr =""
    for time in time_formatted:
        timetablestr+="<tr>"
        timetablestr+="<th scope=\"row\">"+str(time)+"</th>"
        for days in range(1,6):
            #print(days)
            found = 0
            for lecture in lectures:
                #print(f'time:{days} Lecture:{lecture["Weekday"]}')
                # found = 0
                if(lecture["Start_time"]==time and lecture["Weekday"]==str(days)):
                    timetablestr +="<td style=\"border: none;\""+" rowspan="+"\""+str(lecture["Rowspan"])+"\""+">"+"<span>"+str(lecture["Name"])+"<br />"+str(lecture["Start_time"])+" to " + str(lecture["End_time"])+"<br />"+lecture["Location"]+"<br />"+lecture["Type"]+"</span>"+"</td>"
                    found = 1
                    break
                    #print(f'{lecture["Name"]} {lecture["Weekday"]} {lecture["Start_time"]}')
                    
            if found == 0:
                timetablestr +="<td style=\"border: none;\">"+"</td>"
                
        timetablestr+="</tr>"
   
    context = {
        "last_login": request.user.last_login.astimezone(pytz.timezone("Asia/Hong_Kong")).strftime("%d/%m/%Y %I:%M %p"),
        "time_period": time_duration,
        "time_formatted": time_formatted,
        "courses": Courses_enrolled,
        "classes": lectures,
        "timetablestr":timetablestr,
        "upcoming_classes": upcoming_classes,
    }
    
    return render(request, "schedule/home.html", context)

def retrieve_upcoming_classes(user_id):
    result = []
    try:
        # Retrieve all user's enrolment
        user_all_enrolment = Enrolment.objects.filter(student=user_id)
        print(user_all_enrolment)

        # Get the course in each enrolment record
        for enrolment in user_all_enrolment:
            user_registerd_course = Course.objects.get(pk=enrolment.course.id)
            print("This course is:", user_registerd_course)
            classes = Class.objects.filter(course=user_registerd_course.id) # Retrieve all classess for this course
            # Check if any of the classess is starting in less than one hour
            for a_class in classes:
                print("a class:", a_class)
                today_weekday = date.today().isoweekday() # mon: 1 ... sun: 7
                the_class_day = int(a_class.class_day) # mon: 1 ... sun: 7
                if today_weekday == the_class_day:
                    current_time = timedelta(hours=datetime.now().time().hour, minutes=datetime.now().time().minute)
                    the_class_time = timedelta(hours=a_class.start_time.hour, minutes=a_class.start_time.minute)
                    difference_in_time = the_class_time - current_time
                    print("the class time:", the_class_time)
                    print("the current time",current_time)
                    print("Difference:", difference_in_time)
                    if difference_in_time.days <= -1:
                        print("This class is already over or the class is ongoing")
                        continue
                    elif difference_in_time.seconds <= 3600: # 1 hour = 3600 seconds
                        print("This class is starting in less than one hour")
                        temp = {
                            "code": user_registerd_course.code,
                            "name": user_registerd_course.name,
                            "location": a_class.location,
                            "teacher_message": a_class.teacher_message,
                            "zoom_link": a_class.zoom_link,
                            "course_material": user_registerd_course.moodle_link,
                        }
                        result.append(temp)

                        # Create smtp object to connect to gmail
                        smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
                        smtp_object.ehlo()
                        smtp_object.starttls()
                        email = "lmeow2001@gmail.com"
                        password = "xymbwepcwjbovkze"
                        smtp_object.login(email, password)

                        from_address = email
                        to_address = "User.objects.get(pk=user_id).email"
                        subject = "You have class in ONE hour!"
                        message = "The class " + user_registerd_course.code + " " + user_registerd_course.name + " is starting soon."
                        msg = "Subject: " + subject + '\n' + message

                        smtp_object.sendmail(from_address, to_address, msg)

                else:
                    print("This class is not today")
                    continue
        
        # After iterating all the enrolment record, return the array of upcoming classess
        return result
    except ObjectDoesNotExist:
        print("One of the object does not exist")
        return None
    except MultipleObjectsReturned:
        print("More than one objects were retrieved")
        return None