from django.urls import path, include
from . import views

urlpatterns = [
    #GENERAL LINKS
       path('', views.adminpage, name="adminpage"),
       path('createadmin/', views.createadmin, name="createadmin"),
       path('createstaff/', views.createstaff, name="createstaff"),
       path('accounts/', views.accounts, name="accounts"),
]