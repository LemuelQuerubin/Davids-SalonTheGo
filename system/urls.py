from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    #CLIENT
    re_path(r'^$', RedirectView.as_view(pattern_name='appointments', permanent=False), name='index'),
    path('appointments/', views.appointments, name='appointments'),
    path('appointmentsNext/', views.appointmentsNext, name='appointmentsNext'),
    path('index/', views.index, name='index'),
    path('calendar/', views.calendar, name='calendar'),

    #ADMIN
    path('appointmentsPending/', views.appointmentsPending, name='appointmentsPending'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)