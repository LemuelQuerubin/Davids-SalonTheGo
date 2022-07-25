from django.db import models

from account.models import *

class Appointment(models.Model):
    appt_stat = [
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('Confirmed', 'Confirmed'),
        ('Successful', 'Successful'),
        ('Approved', 'Approved')   
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
    #staff = models.ForeignKey(Staff, verbose_name="Staff", null=True)
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
    privilegeCardInfo = models.CharField(max_length=7, verbose_name="Privelege Card Information", blank=True, null=True)
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