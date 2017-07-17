"""
File: Models.py
@author CTN team

This file will hold all of our models for use with the database


"""


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import *
import logging 

BLOOD_CH = (
	('o+', 'O+'),
	('o-', 'O-'),
	('a+', 'A+'),
	('a-', 'A-'),
	('b+', 'B+'),
	('b-', 'B-'),
	('ab+', 'AB+'),
	('ab-', 'AB-'),
	)
CIVIL_CH = (
	('single', 'Single'),
	('married', 'Married'),
	('divorced', 'Divorced'),
	('widowed', 'Widowed'),
	('other', 'Other'),
	)
ETHNIC_CH = (
	('white', 'White'),
	('african_american', 'Black or African American'),
	('hispanic', 'Hispanic or Latino'),
	('native', 'American Indian or Alaska Native'),
	('islander', 'Native Hawaiian or Other Pacific Islander'),
	('other', 'Other'),
	)
USER_CH = (
		('patient', 'Patient'),
		('doctor', 'Doctor'),
		('nurse', 'Nurse'),
		('clerk', 'Clerk')
		)
GENDER_CH = (
		('male', 'Male'),
		('female', 'Female'),
		('other', 'I choose to not specify')
		)		
STATE_CH = (
		('AL', 'Alabama'),
		('AK', 'Alaska'),	
		('AZ', 'Arizona'),
		('AR', 'Arkansas'),
		('CA', 'California'),
		('CO', 'Colorado'),
		('CT', 'Connecticut'),
		('DE', 'Delaware'),
		('FL', 'Florida'),
		('GA', 'Georgia'),
		('HI', 'Hawaii'),
		('ID', 'Idaho'),
		('IL', 'Illinois'),
		('IN', 'Indiana'),
		('IA', 'Iowa'),
		('KS', 'Kansas'),
		('KY', 'Kentucky'),
		('LA','Louisiana'),
		('ME', 'Maine'),
		('MD', 'Maryland'),
		('MA', 'Massachusetts'),
		('MI', 'Michigan'),
		('MN', 'Minnesota'),
		('MS', 'Mississippi'),
		('MO', 'Missouri'),
		('MT', 'Montana'),
		('NE','Nebraska'),
		('NV', 'Nevada'),
		('NH', 'New Hampshire'),
		('NJ', 'New Jersey'),
		('NM', 'New Mexico'),
		('NY', 'New York'),
		('NC', 'North Carolina'),
		('ND', 'North Dakota'),
		('OH', 'Ohio'),
		('OK', 'Oklahoma'),
		('OR', 'Oregon'),
		('PA', 'Pennsylvania'),
		('RI', 'Rhode Island'),
		('SC', 'South Carolina'),
		('SD', 'South Dakota'),
		('TN', 'Tennessee'),
		('TX', 'Texas'),
		('UT', 'Utah'),
		('VT', 'Vermont'),
		('VA', 'Virginia'),
		('WA', 'Washington'),
		('WV', 'West Virginia'),
		('WI', 'Wisconsin'),
		('WY', 'Wyoming')
		)


class UserProfile(models.Model) :
	"""
	Top-level class for a user object
	# reverse lookup: user.profile
	# direct lookup: UserProfile.user
	"""
	user = models.OneToOneField(User, related_name="profile", default = None) 
	age = models.PositiveIntegerField(default = 0, null = True)
	phone = models.CharField(max_length = 15, help_text = "e.g +1(585)123-4567", null = True)
	middle_name = models.CharField(max_length = 30, default = None)
	gender = models.CharField(max_length = 10, choices = GENDER_CH, default = 'other')
	user_type = models.CharField(max_length = 10, choices=USER_CH, default='patient')
	def __str__(self):
                return 'Info of user: {}'.format(self.user.username)
	
class DoctorProfile(models.Model) :
        """
        # reverse lookup: UserProfile.doc_profile
        # direct lookup: DoctorProfile.info
        """
        info = models.OneToOneField(UserProfile, related_name="doc_profile")
        #fields commented out for the sake of not redoing the database again
        bio = models.CharField(max_length = 500, default = None)
        education = models.CharField(max_length = 100, default = 'Medical School')
        languages = models.CharField(max_length = 50, default = 'English')
        asl = models.BooleanField(default = False)
        def __str__(self):
                return 'Dr. {} {}'.format(self.info.user.first_name, self.info.user.last_name)
		#Abstraction to represent an appointment


class PatientProfile(models.Model) :
	""" 
	reverse lookup: UserProfile.patient_profile
	direct lookup: PatientProfile.info
	"""
	info = models.OneToOneField(UserProfile, related_name="patient_profile")
	hospitalized = models.BooleanField(default = False)
	doctor = models.ForeignKey(DoctorProfile, related_name='patients', default = None)
    #### Address
	street = models.TextField(max_length=250, default=None)
	city = models.CharField(max_length=40, default=None)
	state = models.CharField(max_length=15, choices = STATE_CH, default=None)
	zip_code = models.IntegerField(default=None)
    ####
	civil_status = models.CharField(max_length=20, choices = CIVIL_CH, default=None)
	blood_type = models.CharField(max_length=3, choices = BLOOD_CH, default=None)
	ethnicity = models.CharField(max_length=20, choices = ETHNIC_CH, default=None)
	special_needs = models.TextField(max_length=50, default = None)
##    medical_history # surgery, special needs, accident history
##    diagnoses
##    allergies
	organ_donor = models.BooleanField(default = False)
	height = models.CharField(max_length=12, help_text="Example: 5ft 10in", default = None)
	weight = models.CharField(max_length=7, help_text="Example: 120 lb", default = None)
	def __str__(self):
		return "{} {}".format(self.info.user.first_name, self.info.user.last_name)

class ClerkProfile(models.Model):
	"""
    # reverse lookup: UserProfile.clerk_profile
    # direct lookup: ClerkProfile.info
	"""
	info = models.OneToOneField(UserProfile, related_name="clerk_profile")
    #approval_list = models.ForeignKey(AppointmentToken, related_name="appr_token")
	def approve_appointment(appt_token) :
		appt_token.approved = True
		appt_token.details = AppointmentDetails()
	def __str__(self):
		return 'Info of clerk: {}'.format(self.info.user.username)
		
class AppointmentToken(models.Model) :
	 """
     reverse lookup: PatientProfile.apt_token
                     DoctorProfile.apt_token
                     ClerkProfile.apt_token
     direct lookup: AppointmentToken.patient
                    AppointmentToken.doctor
                    AppointmentToken.clerk
	 """
	 number = models.IntegerField(default=None)
	 doctor = models.ForeignKey(DoctorProfile, related_name = "apt_token")
	 doctor_choice = models.CharField(max_length = 10, default = None, choices=(('mine', 'My Doctor'), ('other', 'Other Doctor')))
	 patient = models.ForeignKey(PatientProfile, related_name = "apt_token")
	 date = models.DateField(default = None, help_text = 'Format: yyyy-mm-dd') 
	 time = models.TimeField(default = None, blank = True, help_text = 'Format: hh:mm:ss')
	 reason = models.TextField(max_length = 500, default = None)
	 approved = models.BooleanField(default=False)
	 archived = models.BooleanField(default=False)
	 def __str__(self) :
		 return "Appointment with Dr. {} {} on {}".format(self.doctor.info.user.first_name,
														 self.doctor.info.user.last_name,
														 self.date)
											
class NurseProfile(models.Model) :
	"""
    # reverse lookup: UserProfile.nurse_profile
    # direct lookup: NurseProfile.info
	"""
	info = models.OneToOneField(UserProfile, related_name="nurse_profile")
	def __str__(self):
		return 'Info of nurse: {}'.format(self.info.username)
    
##### SUPPORT CLASSES #######
###Abstraction to represent a prescription
class Prescription(models.Model) :
	"""
    # reverse lookup: PatientProfile.prescription
    # direct lookup: Prescription.patient
	"""
	drug = models.CharField(max_length = 30, default = None)
	drug_id = models.PositiveIntegerField(default = 0)
	directions = models.TextField(max_length = 250, default = None)
	expiration = models.DurationField(default = timedelta)
	status = models.BooleanField(default = None)
	patient = models.ForeignKey(PatientProfile, related_name="prescription")
	def __str__(self):
		return 'Prescription for: {}'.format(self.drug)



class AppointmentDetails(models.Model) :
	"""
    # reverse lookup: AppointmentToken.details
    # direct lookup: AppointmentDetail.token
	"""
	token = models.ForeignKey(AppointmentToken, related_name="details")
	pulse = models.IntegerField(default = 0)
	blood_pressure = models.CharField(max_length = 7, default = None)
    #more info?
	def __str__(self):
		return 'Appointment for{} with {} on {}'.format(self.token.patient.info.user.last_name,
                                                        self.token.doctor.info.user.last_name,
                                                        self.token.date)
    
###Abstraction to represent insurance
class Insurance(models.Model) :
	company = models.CharField(max_length = 60, default = None)
	number = models.IntegerField(default = None)
	patient = models.ForeignKey(PatientProfile, related_name="insurance")

	def __str__(self) :
		return "Insurance with {} number {}" % (self.company, self.number)
		
class SystemLog(models.Model) :
	time = models.DateTimeField(default = None)
	msg = models.CharField(max_length = 50, default = None)
	
	def __str__(self):
		return "{} at {}".format(self.msg, self.time)
