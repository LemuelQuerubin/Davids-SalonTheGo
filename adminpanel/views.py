from django.shortcuts import render, redirect
from account.models import *
from django.contrib import messages
#from account.models import Admin
from account.forms import *
# from account.models import Admin
#TO IMPORT DATETIME
from datetime import datetime
#FOR LOGIN REQUIRED
from django.contrib.auth.decorators import login_required
from account.decorators import *


# Create your views here.
@login_required(login_url="/login")
#@role_required(allowed_roles=["is_admin"])
def adminpage(request):
    current_datetime = datetime.now()

    return render(request, 'admin/admin.html', {'current_datetime':current_datetime})


@login_required(login_url="/login")
def accounts(request):
    current_datetime = datetime.now()
    admins = CustomUser.objects.filter(is_admin=1) 
    context = {
        'admins': admins,
        'current_datetime':current_datetime
    }
    return render(request, 'admin/accounts.html', context)

@login_required(login_url="/login")
def staffaccounts(request):
    current_datetime = datetime.now()
    staffs = CustomUser.objects.filter(is_staff=1, is_admin=0, is_active=1)
    context = {
        'staffs':staffs,
        'current_datetime':current_datetime
    }
    return render(request, 'admin/staff_accounts.html', context)

@login_required(login_url="/login")
def customeraccounts(request):
    current_datetime = datetime.now() 
    customers = CustomUser.objects.filter(is_customer=1) 
    context = {
        'customers': customers,
        'current_datetime':current_datetime,
    } 
    return render(request, 'admin/customer_accounts.html', context)

@login_required(login_url="/login")
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
        #if not username.isalnum():
        #    messages.error(request, "Username must be alpha-numeric")
        #    return redirect('/login')
            
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

        messages.success(request, 'The Account has been successfully created')

        return redirect('/admin/accounts')
    
    context = {
            'stafftype_rows': stafftype_rows,
            'current_datetime':current_datetime,
        }
    
    return render(request, 'admin/create-admin.html', context)

@login_required(login_url="/login")
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
        #if not username.isalnum():
        #    messages.error(request, "Username must be alpha-numeric")
        #    return redirect('/login')
        
        
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

        messages.success(request, 'The Account has been successfully created')

        return redirect('/admin/accounts')
        
    context = {
            'stafftype_rows': stafftype_rows,
            'current_datetime':current_datetime,        
        }

    return render(request, 'admin/create-staff.html', context)


@login_required(login_url="/login")
def editadminprofile(request):
    current_datetime = datetime.now() 
    user = request.user
   
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
        new_profile = request.FILES.get('profilepic', False)
        if new_profile != False:
            admin1.profile_pic = new_profile  #new_profile.name
        admin1.save()

        messages.success(request, 'Your Profile is updated successfully')

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
         'form': form,
     }

    return render(request, 'admin/edit-admin-profile.html', context)

# EDIT STAFF 


# def otc_indivProduct(request, pk):
#     product = otcProduct.objects.get(id=pk)

#     context = {'product': product}
#     return render(request, 'base/otc-products/admin/indiv_product.html', context)

@login_required(login_url="/login")
def editstaffinfo(request, pk):
    
    current_datetime = datetime.now() 
    id = request.user.id 
    staff_account = CustomUser.objects.get(id=pk)
    gender_rows = Gendertype.objects.all()   # gets genders
    stafftype_rows = Stafftype.objects.all() # gets staff types

    if request.method == 'POST':
        gender = request.POST['gender']
        contact_number = request.POST['contact_number']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        stafftype = request.POST['stafftype']
        is_active = request.POST ['staffstat']
        
        
        s = Stafftype.objects.get(pk=stafftype)
        g = Gendertype.objects.get(pk=gender)
       
        staff = Staff.objects.get(staff_id=pk)
        staff.stafftype = s
        staff.gendertype = g
        staff.contact_number = contact_number
        staff.save()
        staff1 = CustomUser.objects.get(id=pk)
        staff1.first_name = first_name
        staff1.last_name = last_name
        staff1.is_active = is_active
        
        
        new_profile = request.FILES.get('profilepic', False)
        if new_profile != False:
            staff1.profile_pic = new_profile  
        staff1.save()

        messages.success(request, 'The Account has been successfully Updated')

        return redirect('/admin/accounts/')

    else:
        form = UpdateAdminProfileForm(instance=request.user)


    context = {
         'staff_account': staff_account,
         'stafftype_rows': stafftype_rows,
         'gender_rows':gender_rows, 
         'current_datetime':current_datetime,
     }

    return render(request, 'admin/edit-staff-info.html', context)


# SERVICES 

@login_required(login_url="/login")
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

@login_required(login_url="/login")    
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

@login_required(login_url="/login")
def viewservices(request):
    return render(request, 'admin/create-service.html')
    
@login_required(login_url="/login")    #servicetype_name
def viewservicetypes(request):
    return render(request, 'admin/create-service.html')




@login_required(login_url="/login")
def changepassword(request):
    current_datetime = datetime.now() 
    user = request.user
   
    if request.method == 'POST':
        id = request.user.id
        newpassword = request.POST['newpassword']

        admin2 = CustomUser.objects.get(pk=id)
        admin2.set_password(newpassword)
        admin2.save()

        messages.success(request, 'Your Password is updated successfully')

    context = {
    'current_datetime':current_datetime,        
    }

    return render(request, 'admin/change-password.html', context)