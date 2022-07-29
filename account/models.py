from django.db import models
from django.contrib.auth.models import AbstractUser 
 
# Create your models here.


class CustomUser (AbstractUser):
    is_admin= models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_pic= models.ImageField(upload_to='profile_pic', default="default-prof.jpg", null=True, blank=True)
    
class Gendertype (models.Model):
    id = models.AutoField(primary_key=True)
    gendertype = models.CharField(max_length=20)

    def __str__(self):
        return self.gendertype
    

class Stafftype (models.Model):
    id = models.AutoField(primary_key=True)
    stafftype = models.CharField(max_length=20)

    def __str__(self):
        return self.stafftype

class Customertype (models.Model):
    id = models.AutoField(primary_key=True)
    customertype = models.CharField(max_length=20)

    def __str__(self):
        return self.customertype

    
class Admin (models.Model):
    admin= models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key = True)

    stafftype = models.ForeignKey(Stafftype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Customer Type")
    gendertype = models.ForeignKey(Gendertype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Gender")
    #gendertype = models.CharField(max_length=10, choices=Gendertype.choices, null=True, blank=True, verbose_name="Gender")
    contact_number = models.CharField(max_length=20, null=True)


    def __str__(self):
        return '%s' %(self.admin)

class Staff (models.Model):
    staff = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key = True)
    stafftype = models.ForeignKey(Stafftype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Staff Type")
    gendertype = models.ForeignKey(Gendertype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Gender")
    #gendertype = models.CharField(max_length=10, choices=Gendertype.choices, null=True, blank=True, verbose_name="Gender")
    contact_number = models.CharField(max_length=20, null=True)

    def __str__(self):
        return '%s' %(self.staff)


class Customer (models.Model):
    customer = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key = True)
    customertype = models.ForeignKey(Customertype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Customer Type")
    gendertype = models.ForeignKey(Gendertype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Gender")
    #gendertype = models.CharField(max_length=10, choices=Gendertype.choices, null=True, blank=True, verbose_name="Gender")
    contact_number = models.CharField(max_length=20, null=True)

    def __str__(self):
        return '%s' %(self.customer)

# SERVICES / based on DB Design
class Servicetype (models.Model):
    id = models.AutoField(primary_key=True)
    servicetype = models.CharField(max_length=100)

    def __str__(self):
        return self.servicetype
    
class Services (models.Model):
    id = models.AutoField(primary_key=True)
    services = models.CharField(max_length=100)
    servicetype = models.ForeignKey(Servicetype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Service Type")
    serviceprice = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.services
    


    



