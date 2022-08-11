from django.db import models

from account.models import *
from base.models import *
from base.models import insProduct

class Appointment(models.Model):
    appt_stat = [
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('Approved', 'Approved'),
        ('Confirmed', 'Confirmed'),
        ('Ongoing', 'Ongoing'),
        ('Successful', 'Successful'),
        
    ]
    appt_type = [
        ('Online', 'Online'),
        ('Walk In', 'Walk In')
    ]
    # ONLINE
    customer = models.ForeignKey(Customer, verbose_name="Customer", null=True, blank=True, on_delete=models.CASCADE)
    # WALK-IN
    email=models.EmailField(max_length=50, verbose_name="Walk-in Email Address", null=True, blank=True)
    contact_num=models.CharField(max_length=11, verbose_name="Walk-in Contact Number", null=True, blank=True)
    customer_fname=models.CharField(max_length=50, verbose_name="Walk-in First Name", null=True, blank=True)
    customer_lname=models.CharField(max_length=50, verbose_name="Walk-in Last Name", null=True, blank=True)
    
    #services = models.ManyToManyField(Services, blank=True, verbose_name="Service")
    services = models.JSONField(default=dict, blank=True)
    #firstStylist = models.ForeignKey(Staff, verbose_name="First Stylist", null=True)
    #secondStylist = models.ForeignKey(Staff, verbose_name="Second Stylist", null=True)
    firstStylist = models.CharField(max_length=30, verbose_name="First Stylist", null=True)
    secondStylist = models.CharField(max_length=30, verbose_name="Second Stylist", null=True)

    appointmentStatus = models.CharField(max_length=20, verbose_name="Appointment Status", choices=appt_stat, default='Pending')
    apptDate = models.DateField(verbose_name="Appointment Date", null=True, blank=True)
    appt_timeStart = models.TimeField(verbose_name="Time Start", null=True, blank=True)
    apptType = models.CharField(max_length=20, verbose_name="Appointment Type", choices=appt_type, default='Online')

    def __str__(self):
        if self.apptType == 'Online':
            return '[%s] %s %s' %(self.apptType, self.customer.customer.first_name, self.customer.customer.last_name)
        else:
            return '[%s] %s %s' %(self.apptType, self.customer_fname, self.customer_lname)

#class AppointmentApproved(models.Model):
'''
class JobOrderForm(models.Model):
    timeFinished = 
    appointmentInfo = models.ForeignKey(Appointment, on_delete=models.CASCADE) #pag-aralan ng on_delete
    servicesPrices = models.JSONField(default=dict)
    inSalonProducts = models.JSONField(default=dict) # kunin from in salon product inventory
    privilegeCardInfo = models.CharField(max_length=7, verbose_name="Privilege Card Information", blank=True, null=True)
    STYLIST = ''

    PRIMARY_STYLIST_CHOICES = [
        (firstStylist, ''),
        (secondStylist, ''),
    ]
    primaryStylist = models.CharField(
        max_length=20,
        choices=PRIMARY_STYLIST_CHOICES,
    )

    # primary stylist pipili si ms jeky
    # price ng services
    # in salon products used 
    # privilege card pa

class ServiceReview:
    appointmentInfo = models.ForeignKey(Appointment, on_delete=models.CASCADE)
# class ProductReview:
'''

class jobOrderform(models.Model):
    appointmentInfo = models.OneToOneField(Appointment, verbose_name="Appointment", on_delete=models.PROTECT)
    servicePrices = models.JSONField(default=dict, blank=True)
    totalPrice = models.DecimalField(default=0, max_digits=9, decimal_places=2, verbose_name="Total", null=True)
    finalStylist = models.CharField(max_length=30, verbose_name="Stylist", null=True)
    
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    #date_today = models.DateField(auto_now_add=True)
    #insproductused = models.ForeignKey(insProduct, on_delete=models.SET_NULL, blank=False, null=True)
    #quantity = models.IntegerField(default=0, null=True, blank=True)
    # privilegeCardInfo = models.CharField(max_length=7, verbose_name="Privelege Card Information", blank=True, null=True)
    # consumed = models.BooleanField(default=False)

    def __str__(self):
        return '%s' %(self.appointmentInfo)

    # def __str__(self):
    #     if self.consumed == True:
    #         insprod_used = self.insproduct.Prod_stockQty - 1
    #         return insprod_used

    # def idk(self):
    #     recordused = self.insproduct.totalUsed + 1
    #     return recordused
    
    # @property
    # def get_total(self):
    #     totalproduct_cost = self.insproduct.Prod_Price * self.quantity
    #     totalservice_cost = self.servicesPrices +
    #     return total, total_service

class clientFeedback(models.Model):
    feedbackInfo = models.OneToOneField(jobOrderform, verbose_name="jobOrderform", on_delete=models.PROTECT)
    review = models.CharField(max_length=100, verbose_name="Review", null=True)
    adminReply = models.TextField(max_length=300, verbose_name="Admin Reply", null=True)
    isPositive = models.BooleanField(null=True)
    isNegative = models.BooleanField(null=True)

    def __str__(self):
        return '%s' %(self.feedbackInfo)


class serviceHistory(models.Model):
    # finalStylist =  models.CharField(null=True, max_length=200, verbose_name="Stylist")
    # customerName = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, max_length=200, verbose_name="Customer Name")
    # #serviceName =  models.ForeignKey(Services, on_delete=models.SET_NULL, null=True, max_length=200, verbose_name="Service Name")
    # serviceName =  models.CharField(null=True, max_length=200, verbose_name="Service Name")
    # serviceType = models.CharField(null=True, max_length=200, verbose_name="Service Type")
    # # objects = models.Manager() #For All Records  
    # # active_objects = IsActiveManager() #For Active Records Only

    # dateDone = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    appointmentInfo = models.OneToOneField(Appointment, verbose_name="Appointment", on_delete=models.PROTECT, null=True)
    servicePrices = models.JSONField(default=dict, blank=True, null=True)
    totalPrice = models.DecimalField(default=0, max_digits=9, decimal_places=2, verbose_name="Total", null=True)
    finalStylist = models.CharField(max_length=30, verbose_name="Stylist", null=True)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)