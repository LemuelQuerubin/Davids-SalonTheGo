from itertools import product
from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User

from account.models import Customer
from system.models import *

# Create your models here.

#PRODUCTS MODELS ------------------------------------------------------
#Is Active Manager
class IsActiveManager(models.Manager):
    def get_queryset(self):

        return super(IsActiveManager, self).get_queryset().filter(is_active=True)

#PRODUCT CATEGORY (BRANDS AND PROMOS)
class Category(models.Model):
    Cat_Name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.Cat_Name

#PRODUCT TYPE (SHAMPOO, CONDITIONER ETC.)
class ProductType(models.Model):
    ProdType_Name = models.CharField(max_length=200, verbose_name="Product Type", unique=True)

    def __str__(self):
        return self.ProdType_Name

#PRODUCT MEASUREMENT (mL, oz, etc.)
class MeasurementType(models.Model):
    Measurement_Type = models.CharField(max_length=200, verbose_name="Product Measurement", unique=True)

    def __str__(self):
        return self.Measurement_Type

#In-Salon Products
class insProduct(models.Model):
    Prod_Name = models.CharField(max_length=200, verbose_name="Product Name")
    ProdType_Name = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Product Type")
    Cat_Name = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Category")
    Prod_Desc = models.TextField(max_length=200, null=True, blank=True, verbose_name="Description")
    Prod_stockQty = models.IntegerField(verbose_name="Stock Quantity")
    Prod_Price = models.DecimalField(decimal_places=2, max_digits=6, verbose_name="Price")
    Prod_Image = models.ImageField(default="placeholder-image.png", upload_to="product_images", null=True, verbose_name="Product Image")
    is_active = models.BooleanField(default=True, verbose_name="Status")
    objects = models.Manager() #For All Records  
    active_objects = IsActiveManager() #For Active Records Only
    date_created = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=False, verbose_name="Expiry Date")
    # recording of total times insalon has been used
    totalUsed = models.IntegerField(default=0,verbose_name="Total Times Used")
    
    add_stock = models.IntegerField(default='0', blank=True, null=True)
    supplier = models.CharField(max_length=50, blank=True, null=True)
    deduct_stock = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    class Meta:
        verbose_name = 'In-salon Product'

    def __str__(self):
        return self.Prod_Name


#Over-the-Counter Products
class otcProduct(models.Model):
    Prod_Name = models.CharField(max_length=200, verbose_name="Product Name")
    ProdType_Name = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Product Type")
    Cat_Name = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Category")
    Prod_Desc = models.TextField(max_length=200, null=True, blank=True, verbose_name="Description")
    Prod_stockQty = models.IntegerField(verbose_name="Stock Quantity")
    Prod_Price = models.DecimalField(decimal_places=2, max_digits=6, verbose_name="Price")
    Prod_Image = models.ImageField(default="placeholder-image.png", upload_to="product_images", null=True, verbose_name="Product Image")
    Measurement_Num = models.IntegerField(blank=False, null=True, verbose_name="Measurement Number")
    Measurement_Type = models.ForeignKey(MeasurementType, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Measurement Type")
    is_active = models.BooleanField(default=True, verbose_name="Status")
    objects = models.Manager() #For All Records  
    active_objects = IsActiveManager() #For Active Records Only
    date_created = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=False, verbose_name="Expiry Date")

    add_stock = models.IntegerField(default='0', blank=True, null=True)
    supplier = models.CharField(max_length=50, blank=True, null=True)
    deduct_stock = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    digital = models.BooleanField(default=False, null=True, blank=False)

    class Meta:
        verbose_name = 'Over-the-Counter Product'

    def __str__(self):
        return self.Prod_Name

class insStockHistory(models.Model):
    Prod_Name = models.CharField(null=True, max_length=200, verbose_name="Product Name")
    ProdType_Name = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Product Type")
    Cat_Name = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Category")
    Prod_Desc = models.TextField(max_length=200, null=True, blank=True, verbose_name="Description")
    Prod_stockQty = models.IntegerField(blank=False, null=True, verbose_name="Stock Quantity")
    Prod_Price = models.DecimalField(null=True, decimal_places=2, max_digits=6, verbose_name="Price")
    Prod_Image = models.ImageField(default="placeholder-image.png", upload_to="product_images", null=True, verbose_name="Product Image")
    is_active = models.BooleanField(default=True, verbose_name="Status")
    objects = models.Manager() #For All Records  
    active_objects = IsActiveManager() #For Active Records Only
    date_created = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=False, verbose_name="Expiry Date")

    add_stock = models.IntegerField(default='0', blank=True, null=True)
    deduct_stock = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    def __str__(self):
        return self.Prod_Name

class otcStockHistory(models.Model):
    Prod_Name = models.CharField(null=True, max_length=200, verbose_name="Product Name")
    ProdType_Name = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Product Type")
    Cat_Name = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Category")
    Prod_Desc = models.TextField(max_length=200, null=True, blank=True, verbose_name="Description")
    Prod_stockQty = models.IntegerField(blank=False, null=True, verbose_name="Stock Quantity")
    Prod_Price = models.DecimalField(null=True, decimal_places=2, max_digits=6, verbose_name="Price")
    Prod_Image = models.ImageField(default="placeholder-image.png", upload_to="product_images", null=True, verbose_name="Product Image")
    is_active = models.BooleanField(default=True, verbose_name="Status")
    objects = models.Manager() #For All Records  
    active_objects = IsActiveManager() #For Active Records Only
    date_created = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=False, verbose_name="Expiry Date")

    add_stock = models.IntegerField(default='0', blank=True, null=True)
    deduct_stock = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    def __str__(self):
        return self.Prod_Name




#ECOMMERCE MODELS ------------------------------------------------------
#CUSTOMER
#class Customer(models.Model):
    #A user can only have one customer. Customer can only have one user
    #Keep the on_delete=models.CASCADE for now; change later
#    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#    name = models.CharField(max_length=200, null=True)
#    email = models.CharField(max_length=200, null=True)

#    def __str__(self):
#        return self.name

PICKUP_STATUS = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Cancelled', 'Cancelled'),
    ('Transaction Successful', 'Transaction Successful'),
    ('Confirmed', 'Confirmed')
)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    pickupstat_id = models.CharField(choices=PICKUP_STATUS, max_length=50, default='Pending')
    
    def __str__(self):
        return str(self.id)

    @property
    def pickup(self):
        pickup = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                pickup = True
        return pickup

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(otcProduct, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.Prod_Price * self.quantity
        return total

class OrderPickUp(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    pickup = models.DateField(null=True, blank=False, verbose_name="Pickup Date")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
	    return str(self.pickup)

class SalesInvoice(models.Model):
    product_pickupID = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=False, null=True)
    amount_total = models.DecimalField(decimal_places=2, max_digits=6, verbose_name="Total Price")

class CustomerReview(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(otcProduct, on_delete=models.SET_NULL, null=True)
    orderpickup = models.ForeignKey(OrderPickUp, on_delete=models.SET_NULL, null=True)
    review = models.TextField(max_length=280, verbose_name="Review", null=True)
    admin_reply = models.TextField(max_length=300, verbose_name="Admin Reply", blank=True, null=True)
    is_like = models.BooleanField(verbose_name="Like", null=True)
    is_dislike = models.BooleanField(verbose_name="Dislike", null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    # class Meta:
    #     unique_together = ('customer', 'product')

    def __str__(self):
        return str(self.id)