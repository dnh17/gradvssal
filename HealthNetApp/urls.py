"""
File: urls.py
@author: CTN team

This function manages all of the urls for the HealthNet


"""


from django.conf.urls import url
from . import views


app_name = 'HealthNetApp'
urlpatterns = [
    url(r'^portal/', views.PortalView, name='portal'),
    url(r'^login/', views.LoginView, name='login'),
    url(r'^logout/', views.LogoutView, name='logout'),
    url(r'^register/$', views.RegisterView, name='register'),
    url(r'^home/$', views.PatientHome, name='home'),
	url(r'^NotPatient/$', views.NotPatientView, name='NotPatient'),
	url(r'^FailLogin/$', views.FailLoginView, name='FailLogin'),
	####### CLERK URLS ###########
	url(r'^clerkhome/$', views.ClerkHome, name='clerkhome'),
	url(r'^clerkprofile/$', views.ClerkProfile, name='clerkprofile'),
	url(r'^areview/$', views.ClerkApptReview, name='areview'),
	url(r'^logs/$', views.SystemLogView, name='SystemLogs'),
	url(r'^plookup/$', views.PatientLookup, name='plookup'),
	######### NURSE URLS #########
	url(r'^nursehome/$', views.NurseHome, name='nursehome'),
	url(r'^nurseprofile/$', views.NurseProfile, name='nurseprofile'),
	url(r'^editnurseprofile/$', views.EditNurseProfile, name='editnurseprofile'),
	######### PATIENT URLS ########
    url(r'^profile/$', views.PatientProfile, name='patientprofile'),
    url(r'^editprofile/$', views.EditPatientProfile, name='editprofile'),
    url(r'^calander/$', views.PatientApptCalander, name='patientcalander'),
	url(r'^mydoc/$', views.PatientMyDoctor, name='mydoc'),
    url(r'^results/$', views.PatientTestResults, name='results'),
    url(r'^schedule/$', views.ScheduleAppt, name='schedule'),
    url(r'^appointment/[0-9]+$', views.AppointmentView, name='appointment'),
    ######## DOCTOR URLS ########
	url(r'^staffhome/$', views.StaffHome, name='staffhome'),
    url(r'^docprofile/$', views.StaffProfile, name='docprofile'),
	url(r'^plist/$', views.PatientList, name='patientlist'),
	url(r'^staffcalander/$', views.StaffApptCalander, name='staffcalander'),
    url(r'^editstaffprofile/$', views.EditStaffProfile, name='editstaffprofile'),
	]
