from django.contrib import admin
from .models import *

admin.site.register(Course)
admin.site.register(Staff)
admin.site.register(Teaching)
admin.site.register(Class)
admin.site.register(Enrolment)