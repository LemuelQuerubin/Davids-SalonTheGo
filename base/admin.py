from django.contrib import admin

# Register your models here.

admin.site.site_header = "SalOnTheGo Admin"
admin.site.site_title = "SalOnTheGo Admin"
#admin.site.index_title = "Welcome to "

from .models import * #insProduct, otcProduct, ProductType, Category

#In-salon Products
class insProductAdmin(admin.ModelAdmin):
    list_display = ('id','Prod_Name', 'ProdType_Name', 'Cat_Name', 'Prod_stockQty', 'Prod_Price', 'is_active', 'expiry_date')
    list_editable = ('is_active',)
admin.site.register(insProduct, insProductAdmin)

#Over-the-Counter Products
class otcProductAdmin(admin.ModelAdmin):
    list_display = ('id','Prod_Name', 'ProdType_Name', 'Cat_Name', 'Prod_stockQty', 'Prod_Price', 'is_active', 'expiry_date')
    list_editable = ('is_active',)
admin.site.register(otcProduct, otcProductAdmin)

admin.site.register(ProductType)
admin.site.register(Category)
admin.site.register(MeasurementType)
# SHOP 
# admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(OrderPickUp)
admin.site.register(SalesInvoice)
admin.site.register(CustomerReview)
#admin.site.register(ShippingAddress)