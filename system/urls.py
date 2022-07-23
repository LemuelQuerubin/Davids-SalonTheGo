from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    #CLIENT
    #re_path(r'^$', RedirectView.as_view(pattern_name='appointments', permanent=False), name='index'),
    path('', views.appointments, name='appointments'),
    path('appointmentsNext/', views.appointmentsNext, name='appointmentsNext'),
    path('index/', views.index, name='index'),
    path('clientViewAppointment/', views.clientViewAppointment, name='clientViewAppointment'),
    
    # CALENDAR -- not yet finished
    path('calendar/', views.calendar, name='calendar'),
    path('calendarDayView/', views.calendarDayView, name='calendarDayView'),
    path('feedbackClient/', views.feedbackClient, name='feedbackClient'),

    # ADMIN
    # APPOINTMENTS
    path('appointmentsPending/', views.appointmentsPending, name='appointmentsPending'),
    path('appointmentsApproved/', views.appointmentsApproved, name='appointmentsApproved'),
    path('jobOrderform/', views.jobOrderform, name='jobOrderform'),
    path('walkIn/', views.walkIn, name='walkIn'),
    path('walkInNext/', views.walkInNext, name='walkInNext'),

    # TRANSACTION SUCCESSFUL
    path('transactionSuccessful/', views.transactionSuccessful, name='transactionSuccessful'),





] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)