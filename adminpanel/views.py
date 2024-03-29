from django.shortcuts import render, redirect
from account.models import *
from django.contrib import messages

#from account.models import Admin
from account.forms import UpdateAdminProfileForm
# from account.models import Admin

from datetime import datetime

# Create your views here.
def adminpage(request):
    current_datetime = datetime.now() 
    return render(request, 'admin/admin.html', {'current_datetime':current_datetime})

def accounts(request):
    current_datetime = datetime.now()
    admins = CustomUser.objects.filter(is_admin=1) 
    staffs = CustomUser.objects.filter(is_staff=1, is_admin=0)
    context = {
        'admins': admins,
        'staffs':staffs,
        'current_datetime':current_datetime
    }
    return render(request, 'admin/accounts.html', context)

def customeraccounts(request):
    customers = CustomUser.objects.filter(is_customer=1) 
    context = {
        'customers': customers
    } 
    return render(request, 'admin/customer_accounts.html', context)

def createadmin(request):
    current_datetime = datetime.now() 

    stafftype_rows = Stafftype.objects.all()
    if request.method == "POST":
        #STORING THE INPUT IN VARIABLE

        username = request.POST['username'] 
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        pass2 = request.POST['pass2']
        stafftype = request.POST['stafftype']
        
        s = Stafftype.objects.get(pk=stafftype)
        
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
        stafftype = s
  
        #SAVING
        myuser.save()
        
        id1 = myuser.id
        id2 = CustomUser.objects.get(pk=id1)
        contact = None
        gender = None
        #u = Stafftype.objects.get(pk=1)

        Admin.objects.create(admin=id2, contact_number=contact, gendertype=gender, stafftype=s)

        return redirect('/admin/accounts')
    
    context = {
            'stafftype_rows': stafftype_rows,
            'current_datetime':current_datetime,
        }
    
    return render(request, 'admin/create-admin.html', context)


def createstaff(request):
    current_datetime = datetime.now() 

    stafftype_rows = Stafftype.objects.all() # to retrieve data from staff types
    if request.method == "POST":
        #STORING THE INPUT IN VARIABLE
        username = request.POST['username'] 
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        pass2 = request.POST['pass2']
        stafftype = request.POST['stafftype']
        
        s = Stafftype.objects.get(pk=stafftype)
        
        

        
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
        stafftype = s
        
        #SAVING
        myuser.save()
        
        id1 = myuser.id
        id2 = CustomUser.objects.get(pk=id1)
        contact = None
        gender = None
        # u = Stafftype.objects.get(pk=1)
        Staff.objects.create(staff=id2, contact_number=contact, gendertype=gender, stafftype=s)

        return redirect('/admin/accounts')
        
    context = {
            'stafftype_rows': stafftype_rows,
            'current_datetime':current_datetime,        
        }

    return render(request, 'admin/create-staff.html', context)


'''
def editadminprofile(request, pk):
    admin = Admin.objects.get(id=pk)
    form = UpdateAdminProfileForm(instance=admin)

    if request.method == 'POST':
        form = UpdateAdminProfileForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('accounts')
    else:
        form = UpdateAdminProfileForm(request.POST, instance=admin)

    context = {'form': form}
    return render(request, 'user/edit-admin-profile.html', context)
'''

def editadminprofile(request):
    current_datetime = datetime.now() 

    gender_rows = Gendertype.objects.all()
    if request.method == 'POST':
        id = request.user.id
        gender = request.POST['gender']
        contact_number = request.POST['contact_number']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        g = Gendertype.objects.get(pk=gender)
        
        admin = Admin.objects.get(pk=id)
        admin.gendertype = g
        admin.contact_number = contact_number
        admin.save()
        admin1 = CustomUser.objects.get(pk=id)
        admin1.first_name = first_name
        admin1.last_name = last_name
        admin1.save()

        return redirect('/admin/')

    #     form = UpdateAdminProfileForm(request.POST, instance=request.user)

    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, f'Your account has been updated!')
    #         return redirect('accounts')

    else:
        form = UpdateAdminProfileForm(instance=request.user)


    context = {
         'gender_rows':gender_rows, 
         'current_datetime':current_datetime,
     }

    return render(request, 'admin/edit-admin-profile.html', context)

# SERVICES 
def createservicetype(request):
    current_datetime = datetime.now()
    if request.method == "POST":
        service_type = request.POST['service_type']

        newservicetype = Servicetype()
        newservicetype.servicetype = service_type
        newservicetype.save()        

        #return redirect('/admin/viewservicetypes/')
    context = {
            'current_datetime':current_datetime,        
        }
    return render(request, 'admin/create-service-type.html', context)

    #Servicetype.objects.create(servicetype_name=servicetype) 

    
def createservice(request):
    current_datetime = datetime.now()
    servicetypes_rows = Servicetype.objects.all()
    if request.method == "POST":
        service_type = request.POST['service_type'] 
        service_name = request.POST['service_name']
        service_price = request.POST['service_price']

        st = Servicetype.objects.get(pk=service_type)
        newservice = Services()
        newservice.servicetype = st
        newservice.services = service_name
        newservice.serviceprice = service_price
        newservice.save() 

    context = {
            'current_datetime':current_datetime,
            'servicetypes_rows': servicetypes_rows,       
        }

    return render(request, 'admin/create-service.html', context)

def viewservices(request):
    return render(request, 'admin/create-service.html')
    


     #servicetype_name
def viewservicetypes(request):
    return render(request, 'admin/create-service.html')

