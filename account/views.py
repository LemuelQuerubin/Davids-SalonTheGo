# TO USE REDIRECT AND RENDER
from django.shortcuts import redirect, render
# REGISTERING USER IN THE BACKEND USING THIS LIBRARY
from django.contrib.auth.models import AbstractUser
# FOR MESSAGING THE USER THAT REGISTER IS SUCCESSFUL
from django.contrib import messages
# TO USE DJANGO USER AUTHENTICATE
from django.contrib.auth import authenticate, login, logout
from .models import *
#IMPORTING SETTINGS TO GET INFO FOR EMAIL
from salonthego import settings
#TO SEND MAIL
from django.core.mail import send_mail
#IN ORDER TO USER CURRENT SITE FUNCTION
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.core.mail import EmailMessage, send_mail




# GENERAL PAGES
def homepage(request):
    return render(request, 'general/homepage-login.html')

def products(request):
    return render(request, 'general/products.html')

def promos(request):
    return render(request, 'general/promos.html')

def aboutus(request):
    return render(request, 'general/aboutus.html')



# AUTHENTICATION PAGES
def loginpage(request):
    if request.method == "POST":
        #STORING THE INPUT IN VARIABLE
        username = request.POST['username'] 
        password = request.POST['password']

        #AUTHENTICATE THE USER/CHECK IF THE INOUT MATCH ON THE RECORD IN THE DATABASE
        user = authenticate(username=username, password=password)
        if user is not None and user.is_customer:
            login(request, user)    
            return redirect('/')
  
        elif user is not None and user.is_staff and not user.is_admin :
            login(request, user) 
            return redirect('/staff')

        elif user is not None and user.is_staff and user.is_admin:
            login(request, user)    
            return redirect('/admin')
            
        
        else:
            messages.error(request,"bad credentials")
            return redirect('/login')
    
    return render(request, 'authentication/login.html')


def registerpage(request):
    if request.method == "POST":
        #STORING THE INPUT IN VARIABLE
        username = request.POST['username'] 
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        pass2 = request.POST['pass2']
        
        #IF USER IS ALREADY TAKEN
        if CustomUser.objects.filter(username=username):
            messages.error(request, "Username already exist")
            return redirect('/login')
        
        #IF EMAIL IS ALREADY TAKEN
        if CustomUser.objects.filter(email=email):
            messages.error(request, "Email already registered")
            return redirect('/login')

        #IF USERNAME LENGTH IS GREATER THAN 10
        if len(username)>10:
            messages.error(request, "Username must be under 10 characters")
            
        #IF PASSWORD DIDNT MATCH
        if password != pass2:
            messages.error(request, "Passwords didn't match")
        
        #USERNAME MUST CONSIST NUMBER AND LETTER
        if not username.isalnum():
            messages.error(request, "Username must be alpha-numeric")
            return redirect('/login')
        
        
        #TRANSFERRING TO THE BACKEND/DATABASE
        myuser = CustomUser.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = 0
        myuser.is_customer = 1
        
        #SAVING
        myuser.save()
        
        id1 = myuser.id
        id2 = CustomUser.objects.get(pk=id1)
        contact = None
        gender = None
        u = Customertype.objects.get(pk=1)
        Customer.objects.create(customer=id2, contact_number=contact, gendertype=gender, customertype=u)


        #MESSAGE FOR SUCCESSFUL REGISTER
        messages.success(request, "Your Account has been successfully created")

        #WELCOMING EMAIL
        subject = "Welcome to the SalOnTheGo"
        message = "Hello " + myuser.first_name + "!!\n" + "Welcome to the David's SalOntheGo \nThank you for visiting our website"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        #EMAIL ADDRESS CONFIRMATION EMAIL
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ David's Salonthego"
        message2 = render_to_string('authentication/email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
  
        #TO REDIRECT USER IN TO LOGIN PAGE
        return redirect('/login')
  
    return render(request, 'authentication/register.html')


def signout(request):
    logout(request)
    return redirect('/')


def activate(request, uidb64, token):
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser: None
    
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = 1
        myuser.save()
        login(request, myuser)
        return redirect('/')
    else:
        return render(request, 'authentication/activation_failed.html')
