"""
File: admin.py   
@author- CTN team

This file runs the admin database

"""


from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(PatientProfile)
admin.site.register(Prescription)
admin.site.register(DoctorProfile)
admin.site.register(NurseProfile)
admin.site.register(AppointmentToken)
admin.site.register(AppointmentDetails)
admin.site.register(Insurance)
admin.site.register(ClerkProfile)
admin.site.register(SystemLog)
#admin.site.register(ClerkProfile)



# Register your models here.
