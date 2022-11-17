from operator import truediv
from django.db import models
from django.db.models import CheckConstraint, Q,F
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from users.models import User

class Course(models.Model):
    code = models.CharField(max_length=11)
    name = models.CharField(max_length=100)
    offered = models.BooleanField()
    moodle_link = models.URLField()
    students = models.ManyToManyField(User, through="Enrolment")
    def __str__(self):
        return f"{self.code} {self.name}"

class Staff(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, through="Teaching")
    
    def __str__(self):
        return f"{self.name}, ID {self.id}"

class Teaching(models.Model):
    class Roles(models.TextChoices):
        TUTOR = "T", _("Tutor")
        LECTURER = "L", _("Lecturer")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=Roles.choices)

    def __str__(self):
        return f"{self.staff.name}, {self.course.code}, {self.role}"

class Enrolment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.email} {self.course.code}"

class Class(models.Model):
    class WeekDays(models.TextChoices):
        MONDAY = "1", _("Monday")
        TUESDAY = "2", _("Tuesday")
        WEDNESDAY = "3", _("Wednesday")
        THURSDAY = "4", _("Thursday")
        FRIDAY = "5", _("Friday")
        SATURDAY = "6", _("Saturday")
        SUNDAY = "7", _("Sunday")

    class ClassTypes(models.TextChoices):
        TUTORIAL = "T", _("Tutorial")
        LECTURE = "L", _("Lecture")
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_id = models.IntegerField()
    location = models.CharField(max_length=100)
    class_day = models.CharField(max_length=3, choices=WeekDays.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_type = models.CharField(max_length=1, choices=ClassTypes.choices)
    zoom_link = models.URLField(blank = True)
    teacher_message = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f"{self.course.code}, {self.class_type}, {self.class_id}, {self.location}, {self.class_day}, {self.start_time}-{self.end_time}"

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError({"start_time": _("Start time is after end time")})

    class Meta:
        unique_together = ['course', 'class_id']
        constraints = [
            CheckConstraint(
                name="valid_start_end_time",
                check=Q(start_time__lt=F("end_time"))
            )
        ]