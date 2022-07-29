from django.forms import ModelForm
from django import forms
from .models import *


class UpdateAdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['gendertype', 'contact_number', ]


'''
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
'''
'''
    def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {'form': form}
    return render(request, 'base/product_form.html', context)


    class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
'''