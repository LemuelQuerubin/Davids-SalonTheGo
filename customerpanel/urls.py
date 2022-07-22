from django.urls import path, include
from . import views

urlpatterns = [
    # CUSTOMER PANEL STAFF
       path('', views.customerpage, name="customerpage"),
       
    # EDIT CUSTOMER PROFILE
       path('editcustomerprofile/', views.editcustomerprofile, name="editcustomerprofile"),
    
]