from django.forms import ModelForm #,CheckboxInput
from django import forms
from .models import otcProduct, insProduct, CustomerReview

class DateInput(forms.DateInput):
	input_type = 'date'
	
class NotClearableImageField(forms.ImageField):
	widget = forms.FileInput

#OTC PRODUCT FORM
class otcProductForm(ModelForm):
	class Meta:
		model = otcProduct
		fields = ['Prod_Name', 'ProdType_Name', 'Cat_Name', 'Measurement_Num', 'Measurement_Type', 'Prod_Desc', 'Prod_stockQty', 'Prod_Price', 'expiry_date', 'Prod_Image', 'is_active'] 
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

#OTC DEDUCT STOCK
class IssueForm(forms.ModelForm):
	class Meta:
		model = otcProduct
		fields = ['deduct_stock']

#OTC RESTOCK
class ReceiveForm(forms.ModelForm):
	class Meta:
		model = otcProduct
		fields = ['add_stock', 'expiry_date']
		widgets = {
			'expiry_date': DateInput()
		}

#REVIEW
class ReviewForm(ModelForm):
	class Meta:
		model = CustomerReview
		fields = ['review','is_like','is_dislike']
