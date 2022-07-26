from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # CUSTOMER PANEL STAFF
       path('', views.customerpage, name="customerpage"),
       
    # EDIT CUSTOMER PROFILE
       path('editcustomerprofile/', views.editcustomerprofile, name="editcustomerprofile"),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)