from django.urls import path, include
from . import views

urlpatterns = [
    #GENERAL LINKS
       path('', views.staffpage, name="staff"),

    # EDIT ADMIN PROFILE
       path('editstaffprofile/', views.editstaffprofile, name="editadminprofile"),
]