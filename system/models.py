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

    customer_fname = models.CharField(max_length=50, verbose_name="First Name", null=True)
    customer_lname = models.CharField(max_length=50, verbose_name="Last Name", null=True)
    services = models.JSONField(default=dict)
    #staff = models.ForeignKey(Staff, verbose_name="Staff", null=True)
    firstStylist = models.CharField(max_length=30, verbose_name="First Stylist", null=True)
    secondStylist = models.CharField(max_length=30, verbose_name="Second Stylist", null=True)
    appointmentStatus = models.CharField(max_length=20, verbose_name="Appointment Status", choices=appt_stat, default='Pending')
    apptDate = models.DateField(verbose_name="Appointment Date", blank=True, null=True)
    appt_timeStart = models.TimeField(verbose_name="Time Start", blank=True, null=True)
    apptType = models.CharField(max_length=20, verbose_name="Appointment Type", choices=appt_type, default='Online')

    def __str__(self):
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
    # privelege card pa

class ServiceReview:
    appointmentInfo = models.ForeignKey(Appointment, on_delete=models.CASCADE)
# class ProductReview:
'''
