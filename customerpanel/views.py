from django.shortcuts import render, redirect
from account.models import *
from django.contrib import messages

from account.forms import UpdateAdminProfileForm

from datetime import datetime
# Create your views here.
#FOR LOGIN REQUIRED
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def customerpage(request):
    current_datetime = datetime.now() 
    return render(request, 'customer/customer.html', {'current_datetime':current_datetime})

@login_required(login_url="/login")
def editcustomerprofile(request):
    current_datetime = datetime.now() 

    gender_rows = Gendertype.objects.all()
    if request.method == 'POST':
        id = request.user.id
        gender = request.POST['gender']
        contact_number = request.POST['contact_number']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        g = Gendertype.objects.get(pk=gender)
        customer = Customer.objects.get(pk=id)
        customer.gendertype = g
        customer.contact_number = contact_number
        customer.save()
        customer1 = CustomUser.objects.get(pk=id)
        customer1.first_name = first_name
        customer1.last_name = last_name
        new_profile = request.FILES.get('profilepic', False)
        if new_profile != False:
            customer1.profile_pic = new_profile
        customer1.save()

        messages.success(request, 'Your Profile is updated successfully')
        return redirect('/customer/')

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

    return render(request, 'customer/edit-customer-profile.html', context)


@login_required(login_url="/login")
def changepasswordcustomer(request):
    current_datetime = datetime.now() 
    user = request.user
   
    if request.method == 'POST':
        id = request.user.id
        newpassword = request.POST['newpassword']

        customer2 = CustomUser.objects.get(pk=id)
        customer2.set_password(newpassword)
        customer2.save()

        messages.success(request, 'Your Password is updated successfully')

    context = {
    'current_datetime':current_datetime,        
    }

    return render(request, 'customer/change-password-customer.html', context)