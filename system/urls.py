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
    path('jobOrderform/', views.jobOrderform, name='jobOrderform'),
    path('walkIn/', views.walkIn, name='walkIn'),
    path('walkInNext/', views.walkInNext, name='walkInNext'),
    path('admincalendar/', views.admincalendar, name='admincalendar'),


    # TRANSACTION SUCCESSFUL
    path('transactionSuccessful/', views.transactionSuccessful, name='transactionSuccessful'),
    
    # FEEDBACK
    path('feedbackClient/', views.feedbackClient, name='feedbackClient'),
    path('feedbackEditClient/', views.feedbackEditClient, name='feedbackEditClient'),
    path('feedbackTable/', views.feedbackTable, name='feedbackTable'),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)