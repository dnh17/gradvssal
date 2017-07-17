"""
File: views.py
@author: CTN team

This file runs the view management for HealthNet


"""
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.core.exceptions import ObjectDoesNotExist

from .forms import *

from .models import *

def PortalView(request):
    if request.user.is_authenticated():
        return render(request, 'HealthNetApp/Patient_Home.html', {'user':request.user})
    template_name = 'HealthNetApp/portal.html'
    return render(request, template_name)

def LoginView(request):
	template_name = 'HealthNetApp/login.html'
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data.get('login'),
                                password=form.cleaned_data.get('password'))
			if user is not None:
				login(request, user)
				log = SystemLog(time = datetime.now(), msg=user.username+" logged in ")
				log.save()
				try:
					user_type = user.profile.user_type
					if user_type == 'doctor':
						#return render(request, 'HealthNetApp/Staff_Home.html', {'user':user})
						return HttpResponseRedirect("../staffhome/")
					elif user_type == 'nurse':
						return render(request, 'HealthNetApp/Nurse_Home.html', {'user':user})
					elif user_type == 'clerk':
						#return render(request, 'HealthNetApp/Clerk_Home.html', {'user':user})
						return HttpResponseRedirect("../clerkhome/")
					elif user_type == 'patient':
						return HttpResponseRedirect("../home/")
				except UserProfile.DoesNotExist:
					return render(request, 'HealthNetApp/Patient_Home.html', {'user':user})
			else:
				log = SystemLog(time = datetime.now(), msg="Failed login attempt ")
				log.save()
				return HttpResponseRedirect("../FailLogin/")
	else:
		form = LoginForm()
	return render(request, template_name, {'form': form})
	#return HttpResponseRedirect("../home/")

def LogoutView(request):
	template_name = 'HealthNetApp/portal.html'
	log = SystemLog(time = datetime.now(), msg=request.user.username+" logged out ")
	log.save()
	logout(request)
	return render(request, template_name)
	
def FailLoginView(request):
    template_name = 'HealthNetApp/FailLogin.html'
    return render(request, template_name)	
	
def RegisterView(request):
	template_name = 'HealthNetApp/register.html'
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(username=form.cleaned_data.get('userName'),
								email=form.cleaned_data.get('email'),
								password=form.cleaned_data.get('password'),
								first_name=form.cleaned_data.get('firstName'),
								last_name=form.cleaned_data.get('lastName'))
			user.save()
			log = SystemLog(time = datetime.now(), msg=user.username+" logged in ")
			log.save()
			if (form.cleaned_data.get('userType') != 'patient'):
				return HttpResponseRedirect("../NotPatient/")
				return HttpResponse("Please contact the Systems Administartor to initialize your account.")
			return render(request, 'HealthNetApp/portal.html', )
	else:
		form = RegisterForm()
	return render(request, template_name, {'form':form})
	
def NotPatientView(request):
    template_name = 'HealthNetApp/NotPatient.html'
    return render(request, template_name)	

def PatientHome(request):
	if not request.user.is_authenticated(): #Kick the user to portal if they are not authenticated
		return HttpResponseRedirect("../portal/")
	user = request.user # fetch current user
	try:	#if user has no profile, redirect to profile creation
		profile = user.profile
	except UserProfile.DoesNotExist: 
		return HttpResponseRedirect("../editprofile/")
	template_name= 'HealthNetApp/Patient_Home.html'
	id = user.profile.patient_profile
	appointmentsSet = AppointmentToken.objects.all()
	return render(request, template_name, {'querySet':appointmentsSet})
	
def PatientProfile(request):
    if not request.user.is_authenticated(): #Kick the user to portal if they are not authenticated
        return HttpResponseRedirect("../portal/")
    user = request.user # fetch current user
    template_name = 'HealthNetApp/Patient_Profile.html'
    try:
        if user.profile != None: # display as normal if profile exists
            pass
    except UserProfile.DoesNotExist: 
        return HttpResponseRedirect("../editprofile/") # if user does not have a profile, edit it
    return render(request, template_name, {'user':user})

def EditPatientProfile(request):
	template_name= 'HealthNetApp/Patient_EditProf.html'
	if request.method == 'POST':
		try:
			profile = request.user.profile # update existing
			form = EditProfileForm(request.POST, instance = profile)
			if form.is_valid():
				form.save()
			form = EditPatientProfileForm(request.POST, instance = profile.patient_profile)
			if form.is_valid():
				form.save()
				log = SystemLog(time = datetime.now(), msg=request.user.username+" created profile ")
				log.save()
				return HttpResponseRedirect("../profile/")
		except UserProfile.DoesNotExist:
			form = EditProfileForm(request.POST)	#create new
			form2 = EditPatientProfileForm(request.POST)
			if form.is_valid() and form2.is_valid():
				model_instance = form.save(commit=False)
				model_instance.user_type = 'patient'
				model_instance.user = request.user
				model_instance.save()
				log = SystemLog(time = datetime.now(), msg=model_instance.user.username+" edited profile ")
				log.save()
				
				model_instance = form2.save(commit=False)
				model_instance.info = request.user.profile
				model_instance.doctor = DoctorProfile.objects.get(id=len(DoctorProfile.objects.all()))
				model_instance.hospitalized = False
				if model_instance.special_needs == None:
					model_instance.special_needs = 'N/A'
				model_instance.save()
				return HttpResponseRedirect("../profile/")
	else:
		form = EditProfileForm()
		form2 = EditPatientProfileForm()
	return render(request, template_name, {'form':form, 'form2':form2})

def PatientApptCalander(request):
	user = request.user
	if not request.user.is_authenticated(): #Kick the user to portal if they are not authenticated
		return HttpResponseRedirect("../portal/")
	try:	#if user has no profile, redirect to profile creation
		profile = user.profile
	except UserProfile.DoesNotExist: 
		return HttpResponseRedirect("../editprofile/")
	template_name = 'HealthNetApp/Patient_ApptCal.html'
	id = user.profile.patient_profile
	appointmentsSet = AppointmentToken.objects.filter(approved=True)
	pendSet = AppointmentToken.objects.filter(approved=False)
	return render(request, template_name, {'querySet':appointmentsSet, 'pendSet':pendSet})
	
def AppointmentView(request):
	user = request.user
	if not request.user.is_authenticated(): #Kick the user to portal if they are not authenticated
		return HttpResponseRedirect("../portal/")
	template_name = 'HealthNetApp/Patient_IndivAppt.html'
	id = user.profile.patient_profile
	appointmentsSet = AppointmentToken.objects.all()
	return render(request, template_name, {'querySet':appointmentsSet})

def PatientMyDoctor(request):
	if not request.user.is_authenticated(): #Kick the user to portal if they are not authenticated
		return HttpResponseRedirect("../portal/")
	try:	#if user has no profile, redirect to profile creation
		profile = request.user.profile
	except UserProfile.DoesNotExist: 
		return HttpResponseRedirect("../editprofile/")
	template_name= 'HealthNetApp/Patient_MyDoc.html'
	my_doc = request.user.profile.patient_profile.doctor
	return render(request, template_name, {'doctor':my_doc})

def PatientTestResults(request):
	if not request.user.is_authenticated(): #Kick the user to portal if they are not authenticated
		return HttpResponseRedirect("../portal/")
	try:	#if user has no profile, redirect to profile creation
		profile = request.user.profile
	except UserProfile.DoesNotExist: 
		return HttpResponseRedirect("../editprofile/")
	template_name= 'HealthNetApp/Patient_TestResults.html'
	return render(request, template_name)

def StaffApptCalander(request):
    template_name = 'HealthNetApp/Staff_ApptCal.html'
    return render(request, template_name)
###
def ScheduleAppt(request):
	patient_profile = request.user.profile.patient_profile
	if not request.user.is_authenticated(): #Kick the user to portal if they are not authenticated
		return HttpResponseRedirect("../portal/")
	template_name = 'HealthNetApp/Patient_SchApp.html'
        
	if request.method == 'POST':
		form = ScheduleAppointment(request.POST)
		if form.is_valid(): # now, perform all the error-checking on the appointment
			model_instance = form.save(commit=False)
			if (model_instance.date < datetime.now().date()):
				return HttpResponse("Can't schedule in the past!")
			# conflict_list = AppointmentToken.objects.filter(doctor = patient_profile.doctor, date = datetime.today())
			# for i in conflict_list:
				# if (i.time() + timedelta()
			model_instance.patient = patient_profile
			model_instance.approved = False
			model_instance.doctor_choice = 'mine'
			model_instance.number = len(AppointmentToken.objects.all()) + 1 # assign ID
			model_instance.save()
			log = SystemLog(time = datetime.now(), msg=request.user.username+" requested an appointment ")
			log.save()
			return HttpResponseRedirect("../calander/")
	else:
		form = ScheduleAppointment()
	return render(request, template_name, {'form':form})
###
def StaffHome(request):
	if not request.user.is_authenticated(): #Kick the user to portal if they are not authenticated
		return HttpResponseRedirect("../portal/")
	template_name = 'HealthNetApp/Staff_Home.html'
	return render(request, template_name)
	
def PatientList(request):
	if not request.user.is_authenticated(): #Kick the user to portal if they are not authenticated
		return HttpResponseRedirect("../portal/")
	template_name='HealthNetApp/Staff_MyPatient.html'
	doctor = request.user.profile.doc_profile
	querySet = PatientProfile.objects.filter(doctor = doctor)
	return render(request, template_name, {'pats':querySet})
	
def NurseHome(request):
    if not request.user.is_authenticated(): #Kick the user to portal if they are not authenticated
        return HttpResponseRedirect("../portal/")
    
    template_name = 'HealthNetApp/Nurse_Home.html'
    return render(request, template_name)
	

def EditStaffProfile(request):
    #return HttpResponse("Needs to be completed")
    template_name='HealthNetApp/Staff_EditProf.html'
    if request.method=='POST':
        try:
                profile=request.user.profile
                if request.user.profile.user_type == 'doctor':
                    form=EditDoctorProfileForm(request.POST, instance=profile)
                elif request.user.profile.user_type == 'nurse':
                    form=EditNurseProfileForm(request.POST, instance=profile)
                elif request.user.profile.user_type == 'clerk':
                    form=EditNurseProfileForm(request.POST, instance=profile)
                else:
                    return HttpResponse("How the heck did a patient call this view?")
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("../docprofile/")
        except UserProfile.DoesNotExist:
            return HttpResponse("Seek admin help to initialize profile")
    else:
            profile=request.user.profile
            if request.user.profile.user_type == 'doctor':
                form=EditDoctorProfileForm(request.POST, instance=profile)
            elif request.user.profile.user_type == 'nurse':
                form=EditNurseProfileForm()
            elif request.user.profile.user_type == 'clerk':
                form=EditNurseProfileForm()
            else:
                return HttpResponse("How the heck did a patient call this view?")
    return render(request, template_name, {'form':form})
	
def EditNurseProfile(request):
    #return HttpResponse("Needs to be completed")
    template_name='HealthNetApp/Nurse_EditProf.html'
    if request.method=='POST':
        try:
                profile=request.user.profile
                if request.user.profile.user_type == 'doctor':
                    form=EditDoctorProfileForm(request.POST, instance=profile)
                elif request.user.profile.user_type == 'nurse':
                    form=EditNurseProfileForm(request.POST, instance=profile)
                elif request.user.profile.user_type == 'clerk':
                    form=EditNurseProfileForm(request.POST, instance=profile)
                else:
                    return HttpResponse("How the heck did a patient call this view?")
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("../nurseprofile/")
        except UserProfile.DoesNotExist:
            return HttpResponse("Seek admin help to initialize profile")
    else:
            profile=request.user.profile
            if request.user.profile.user_type == 'doctor':
                form=EditDoctorProfileForm(request.POST, instance=profile)
            elif request.user.profile.user_type == 'nurse':
                form=EditNurseProfileForm()
            elif request.user.profile.user_type == 'clerk':
                form=EditNurseProfileForm()
            else:
                return HttpResponse("How the heck did a patient call this view?")
    return render(request, template_name, {'form':form})

def StaffProfile(request):
    if not request.user.is_authenticated(): #Kick the user to portal if they are not authenticated
        return HttpResponseRedirect("../portal/")
    user = request.user # fetch current user
    template_name = 'HealthNetApp/Staff_Profile.html'
    try:
        if user.profile != None: # display as normal if profile exists
            pass
    except UserProfile.DoesNotExist: 
        return HttpResponseRedirect("../editstaffprofile/") # if user does not have a profile, edit it
    return render(request, template_name, {'user':user})
    
def NurseProfile(request):
    if not request.user.is_authenticated(): #Kick the user to portal if they are not authenticated
        return HttpResponseRedirect("../portal/")
    user = request.user # fetch current user
    template_name = 'HealthNetApp/Nurse_Profile.html'
    try:
        if user.profile != None: # display as normal if profile exists
            pass
    except UserProfile.DoesNotExist: 
        return HttpResponseRedirect("../editstaffprofile/") # if user does not have a profile, edit it
    return render(request, template_name, {'user':user})
	
##############################################3 CLERK VIEWS ###
def ClerkHome(request):
	return render(request, "HealthNetApp/Clerk_Home.html")
	
def PatientLookup(request):
	return render(request, "HealthNetApp/Clerk_PatLook.html")
	
def ClerkProfile(request):
    if not request.user.is_authenticated(): #Kick the user to portal if they are not authenticated
        return HttpResponseRedirect("../portal/")
    user = request.user # fetch current user
    template_name = 'HealthNetApp/Clerk_Profile.html'
    try:
        if user.profile != None: # display as normal if profile exists
            pass
    except UserProfile.DoesNotExist: 
        return HttpResponse("Seek Admin to enable your profile!")
    return render(request, template_name, {'user':user})
	
def ClerkApptReview(request): 
	template_name = 'HealthNetApp/Clerk_AppRev.html'
	approvalSet = AppointmentToken.objects.filter(doctor_choice = 'mine', approved = False, archived = False)
	if request.method == "POST":
		form = ApproveForm(request.POST)
		if form.is_valid():
			appt_num = form.cleaned_data.get('number')
			appt_inst = AppointmentToken.objects.get(number=appt_num)
			appt_inst.approved = True
			appt_inst.save()
			log = SystemLog(time = datetime.now(), msg=request.user.username+" approved an appointment for "+appt_inst.patient.info.user.username)
			log.save()
	else:
		form = ApproveForm()
	return render(request, template_name, {'set1':approvalSet, 'form':form})
	
def SystemLogView(request):
	querySet = SystemLog.objects.all()
	template_name = 'HealthNetApp/Clerk_Logs.html'
	return render(request, template_name, {'logs':querySet})

def PatientList(request):
    template_name = 'HealthNetApp/Staff_MyPatient.html'
    return render(request, template_name)

    
