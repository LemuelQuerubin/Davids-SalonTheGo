from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #GENERAL LINKS
       path('', views.staffpage, name="staff"),

    # EDIT ADMIN PROFILE
       path('editstaffprofile/', views.editstaffprofile, name="editadminprofile"),
       path('changepassword/', views.changepasswordstaff, name="changepasswordstaff"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)