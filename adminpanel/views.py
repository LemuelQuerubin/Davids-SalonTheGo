from django.shortcuts import render, redirect
from account.models import *
from django.contrib import messages

# Create your views here.
def adminpage(request):
    return render(request, 'admin/admin.html')

def accounts(request):
    return render(request, 'admin/accounts.html')

def createadmin(request):
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
        myuser.is_active = 1
        myuser.is_admin = 1
        myuser.is_staff = 1
        myuser.is_superuser = 1
  
        #SAVING
        myuser.save()
        
        id1 = myuser.id
        id2 = CustomUser.objects.get(pk=id1)
        contact = None
        gender = None
        u = Stafftype.objects.get(pk=1)
        Admin.objects.create(user=id2, contact_number=contact, gendertype=gender, stafftype=u)

        return redirect('/admin/createadmin')
    
    return render(request, 'admin/create-admin.html')


def createstaff(request):
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
        myuser.is_active = 1
        myuser.is_staff = 1
        
        #SAVING
        myuser.save()
        
        id1 = myuser.id
        id2 = CustomUser.objects.get(pk=id1)
        contact = None
        gender = None
        u = Stafftype.objects.get(pk=1)
        Staff.objects.create(user=id2, contact_number=contact, gendertype=gender, stafftype=u)

        return redirect('/admin/createstaff')
    
    return render(request, 'admin/create-staff.html')