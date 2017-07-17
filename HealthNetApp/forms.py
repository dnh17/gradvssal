
from django import forms
from django.forms import ModelForm
from django.db import models
from HealthNetApp.models import *

USER_CH = (
		('patient', 'Patient'),
		('doctor', 'Doctor'),
		('nurse', 'Nurse'),
		('clerk', 'Clerk')
		)

class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length = 150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length = 16)
    
class RegisterForm(forms.Form):
	firstName = forms.CharField(label='First Name', max_length = 30)
	lastName = forms.CharField(label='Last Name', max_length = 30)
	userName = forms.CharField(label='Username', max_length = 150)
	userType = forms.ChoiceField(choices = USER_CH)
	email = forms.EmailField(label = 'Email')
	password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length = 16)
	
class ApproveForm(ModelForm):
	#appt_id = forms.CharField(label='Appointment Number', max_length=4)
		class Meta:
			model = AppointmentToken
			fields = ['number']

class EditDoctorProfileForm(ModelForm):
	class Meta:
		model=DoctorProfile
		#fields= ['age', 'phone', 'middle_name', 'gender']
		fields= '__all__'
		
class EditPatientProfileForm(ModelForm):
	special_needs = forms.CharField(required = False)
	class Meta:
		model = PatientProfile
		#fields = ['street', 'doctor',  'city', 'state', 'zip_code', 'civil_status', 'blood_type']
		exclude = ['info', 'hospitalized', 'doctor']
		fields = "__all__"

class EditNurseProfileForm(ModelForm):
	class Meta:
		model=NurseProfile
        #fields= ['age', 'phone', 'middle_name', 'gender']
		fields= '__all__'

class EditClerkProfileForm(ModelForm):
        class Meta:
            model=ClerkProfile
            fields= '__all__'

class EditProfileForm(ModelForm):
        middle_name = forms.CharField(required = False)
        class Meta:
                model = UserProfile
                fields = ['age', 'phone', 'middle_name', 'gender']
		#fields= '__all__'

    
class ScheduleAppointment(ModelForm):
	date = forms.DateField(widget=forms.widgets.DateInput(attrs={'class':'datepicker'}))
	time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'class':'timepicker'}))

	class Meta:
		model = AppointmentToken
		fields = ['date', 'time', 'reason', 'doctor']
		#fields = '__all__'
		
