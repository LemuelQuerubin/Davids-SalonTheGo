from django.shortcuts import render, redirect
from account.models import *
from django.contrib import messages

#from account.models import Admin
from account.forms import UpdateAdminProfileForm
from account.models import Admin

# Create your views here.
def staffpage(request):
    return render(request, 'staff/staff.html')

def editstaffprofile(request):
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
        staff1.save()

    else:
        form = UpdateAdminProfileForm(instance=request.user)


    context = {
         'gender_rows':gender_rows
     }

    return render(request, 'staff/edit-staff-profile.html', context)
