from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    #CLIENT
    path('', views.appointments, name='appointments'),
    path('appointmentsNext/', views.appointmentsNext, name='appointmentsNext'),
    path('index/', views.index, name='index'),
    path('clientViewAppointment/', views.clientViewAppointment, name='clientViewAppointment'),
    
    # CALENDAR -- not yet finished
    path('calendar/', views.calendar, name='calendar'),
    path('calendarDayView/', views.calendarDayView, name='calendarDayView'),
    #path('feedbackClient/', views.feedbackClient, name='feedbackClient'),

    # ADMIN
    # APPOINTMENTS
    path('appointmentsPending/', views.appointmentsPending, name='appointmentsPending'),
    path('appointmentsApproved/', views.appointmentsApproved, name='appointmentsApproved'),
    path('appointmentsOngoing/', views.appointmentsOngoing, name='appointmentsOngoing'),
    path('alljobOrderforms/', views.alljobOrderforms, name='alljobOrderforms'),
    path('jobOrderform/', views.jobOrderForm, name='jobOrderform'),
    path('walkIn/', views.walkIn, name='walkIn'),
    path('walkInNext/', views.walkInNext, name='walkInNext'),
    path('admincalendar/', views.admincalendar, name='admincalendar'),
    path('admincalendardayview/', views.admincalendardayview, name='admincalendardayview'),
    path('appointmentsDone/', views.appointmentsDone, name='appointmentsDone'),
    path('allschedules/', views.adminallschedules, name='allschedules'),
    

    # SERVICES
    path('allservices/', views.allservices, name='allservices'),
    path('servicehistory/', views.servicehistory, name='servicehistory'),
    
    path('go_back/', views.go_back, name='go_back'),

    # TRANSACTION SUCCESSFUL
    path('transactionSuccessful/', views.transactionSuccessful, name='transactionSuccessful'),
    
    # FEEDBACK
    path('feedbackClient/', views.feedbackClient, name='feedbackClient'),
    path('feedbackClientView/', views.feedbackClientView, name='feedbackClientView'),
    path('feedbackTable/', views.feedbackTable, name='feedbackTable'),
    path('feedbackreplyAdmin/', views.feedbackreplyAdmin, name='feedbackreplyAdmin'),
    path('adminfeedbackTable/', views.adminfeedbackTable, name='adminfeedbackTable'),

    # PDF/ REPORT GENERATION
    path('createpdf-servicesales/', views.pdf_report_create_service_sales, name='createpdf'),
    path('jobOrderformtbl/', views.jobOrderformtbl, name='jobOrderformtbl'),
    path('createpdf-joftable/', views.jobOrderformtblreport, name='jobOrderformtblreports'),
    path('createpdf-allschedule/', views.adminallschedulesreport, name='adminallschedulesreport'),
    path('createpdf-jof/', views.jobOrderFormreport, name='joborderformreport'),

    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)