from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #GENERAL LINKS
       path('', views.adminpage, name="adminpage"),
       path('createadmin/', views.createadmin, name="createadmin"),
       path('createstaff/', views.createstaff, name="createstaff"),
       path('accounts/', views.accounts, name="accounts"),

    # EDIT ADMIN PROFILE
       path('editadminprofile/', views.editadminprofile, name="editadminprofile"),
   
    # EDIT STAFF INFO
       path('editstaffinfo/<str:pk>/', views.editstaffinfo, name="editstaffinfo"),
       #path('editstaffinfo/', views.editstaffinfo, name="editstaffinfo"),

   # VIEW CUSTOMER ACCOUNTS
       path('customeraccounts/', views.customeraccounts, name="customeraccounts"),

   # SERVICES
       path('createservice/', views.createservice, name="createservice"),
       path('createservicetype/', views.createservicetype, name="createservicetype"),
       path('viewservices/', views.viewservices, name="viewservices"),
       path('viewservicetypes/', views.viewservicetypes, name="viewservicetypes"),

       path('changepassword/', views.changepassword, name="changepassword"),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)