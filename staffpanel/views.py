from django.shortcuts import render, redirect
from account.models import *
from django.contrib import messages

#from account.models import Admin
from account.forms import UpdateAdminProfileForm
from account.models import Admin

from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login")
def staffpage(request):
    current_datetime = datetime.now() 

    return render(request, 'staff/staff.html', {'current_datetime':current_datetime})


@login_required(login_url="/login")
def editstaffprofile(request):
    current_datetime = datetime.now() 

    gender_rows = Gendertype.objects.all()
    if request.method == 'POST':
        id = request.user.id
        gender = request.POST['gender']
        contact_number = request.POST['contact_number']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        g = Gendertype.objects.get(pk=gender)
        staff = Staff.objects.get(pk=id)
        staff.gendertype = g
        staff.contact_number = contact_number
        staff.save()
        staff1 = CustomUser.objects.get(pk=id)
        staff1.first_name = first_name
        staff1.last_name = last_name
        new_profile = request.FILES.get('profilepic', False)
        if new_profile != False:
            staff1.profile_pic = new_profile
        staff1.save()

        messages.success(request, 'Your Profile is updated successfully')

        return redirect('/staff/')

    else:
        form = UpdateAdminProfileForm(instance=request.user)


    context = {
         'gender_rows':gender_rows, 
         'current_datetime':current_datetime,
     }

    return render(request, 'staff/edit-staff-profile.html', context)


@login_required(login_url="/login")
def changepasswordstaff(request):
    current_datetime = datetime.now() 
    user = request.user
   
    if request.method == 'POST':
        id = request.user.id
        newpassword = request.POST['newpassword']

        staff2 = CustomUser.objects.get(pk=id)
        staff2.set_password(newpassword)
        staff2.save()

        messages.success(request, 'Your Password is updated successfully')

    context = {
    'current_datetime':current_datetime,        
    }

    return render(request, 'staff/change-password-staff.html', context)
