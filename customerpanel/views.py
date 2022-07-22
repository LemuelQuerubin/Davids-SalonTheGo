from django.shortcuts import render
from account.models import *

from account.forms import UpdateAdminProfileForm
# Create your views here.


def customerpage(request):
    return render(request, 'customer/customer.html')

def editcustomerprofile(request):
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
        customer1.save()

    #     form = UpdateAdminProfileForm(request.POST, instance=request.user)

    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, f'Your account has been updated!')
    #         return redirect('accounts')

    else:
        form = UpdateAdminProfileForm(instance=request.user)


    context = {
         'gender_rows':gender_rows
     }

    return render(request, 'customer/edit-customer-profile.html', context)