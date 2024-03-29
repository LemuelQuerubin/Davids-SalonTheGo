from django.urls import path, include
from . import views

urlpatterns = [
    #GENERAL LINKS
    path('', views.homepage, name="homepage"),
    path('products/', views.products, name="products"),
    path('promos/', views.promos, name="promos"),
    path('aboutus/', views.aboutus, name="aboutus"),

    #AUTHENTICATION LINKS
    path('login/', views.loginpage, name="loginpage"),
    path('register/', views.registerpage, name="registerpage"),
    path('logout/', views.signout, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),

    
]