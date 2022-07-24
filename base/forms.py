from django.forms import ModelForm #,CheckboxInput
from django import forms
from .models import otcProduct, insProduct

class DateInput(forms.DateInput):
    input_type = 'date'
    
class NotClearableImageField(forms.ImageField):
    widget = forms.FileInput

#OTC PRODUCT FORM
class otcProductForm(ModelForm):
    class Meta:
        model = otcProduct
        fields = ['Prod_Name', 'ProdType_Name', 'Cat_Name', 'Prod_Desc', 'Prod_stockQty', 'Prod_Price', 'expiry_date', 'Prod_Image', 'is_active'] 
        widgets = {
            'expiry_date': DateInput(),
            'Prod_Image': forms.FileInput(),
        }

#IN-SALON PRODUCT FORM
class insProductForm(ModelForm):
    class Meta:
        model = insProduct
        fields = ['Prod_Name', 'ProdType_Name', 'Cat_Name', 'Prod_Desc', 'Prod_stockQty', 'Prod_Price', 'expiry_date', 'Prod_Image', 'is_active']
        widgets = {
            'expiry_date': DateInput(),
            'Prod_Image': forms.FileInput(),
        }

# class StatusForm(forms.ModelForm):
#     class Meta:
#         model = otcProduct
#         fields = ['is_active']

        #widgets = {
        #    'is_active': CheckboxInput(attrs={'onchange': 'this.form.submit();'})
        #}