from django.db import models
from django.contrib.auth.models import AbstractUser 
 
# Create your models here.


class CustomUser (AbstractUser):
    is_admin= models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

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
    user= models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key = True)
    stafftype = models.ForeignKey(Stafftype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Customer Type")
    gendertype = models.ForeignKey(Gendertype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Gender")
    contact_number = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.user.username


class Staff (models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key = True)
    stafftype = models.ForeignKey(Stafftype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Staff Type")
    gendertype = models.ForeignKey(Gendertype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Gender")
    contact_number = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.user.username


class Customer (models.Model):
    user= models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key = True)
    customertype = models.ForeignKey(Customertype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Customer Type")
    gendertype = models.ForeignKey(Gendertype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Gender")
    contact_number = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.user.username




    



