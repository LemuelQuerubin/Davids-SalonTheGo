from django.db import models

class Appointment(models.Model):
    appt_stat = [
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('Confirmed', 'Confirmed'),
        ('Successful', 'Successful')    
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

    def __str__(self):
        return '[%s] %s %s' %(self.id, self.customer_fname, self.customer_lname)
