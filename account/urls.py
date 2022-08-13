from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    #GENERAL LINKS
    path('', views.homepage, name="homepage"),
    path('products/', views.products, name="products"),
    path('promos/', views.promos, name="promos"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('reviews/', views.reviews, name="reviews"),
    path('indivreviews/', views.indivreviews, name="indivreviews"),

    #AUTHENTICATION LINKS
    path('login/', views.loginpage, name="loginpage"),
    path('register/', views.registerpage, name="registerpage"),
    path('logout/', views.signout, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),

    #path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    #path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done" ),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    #path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    #NOTIFS
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
