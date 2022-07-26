from multiprocessing import context
from tkinter import E
from unicodedata import name
from django.shortcuts import render, redirect
from .models import *

from account.models import *
from base.models import *

from datetime import datetime
from datetime import date
import json
from datetime import timedelta

# APPOINTMENTS ----------------------------------------------------------------------------------
def appointments(request):
    #services_list = Services.objects.filter(servicetype_id__in=[1,2,3,4,5])
    # services in database
    current_datetime = datetime.now()
    if request.method == 'POST':
        services = request.POST.getlist('services')
        request.session['services'] = services
        #srv = Services.objects.get(pk=services)

        #pickedservice = Appointment()
        #pickedservice.services = srv
        return redirect('appointmentsNext')

    '''context = {
        'services_list': services_list
    }'''  
    context = {     
        'current_datetime':current_datetime,    
    }
    return render(request, 'appts.html', context)#, context)


def appointmentsNext(request):
    current_datetime = datetime.now() 
    customer = Customer.objects.get(customer=request.user)
    staff = Staff.objects.filter(stafftype=3)
    services = request.session['services']
    group1 = []
    group2 = []
    group3 = []
    group4 = []
    for row in staff:
        name = row.staff.first_name
        appt = Appointment.objects.filter(firstStylist=name)
        for row1 in appt:
            t_array=[]
            s = row1.services
            add = 0
            for i in range(0, len(s)):
                if (s[i] == "Haircut" or s[i] == "Shampoo and Blowdry" or s[i] == "Setting Ironing"):
                    add = add + 45
                elif (s[i] == "Treatment" or s[i] == "Regular Hot Oil" or s[i] == "Hair Spa" or s[i] == "Make-up"):
                    add = add + 60
                elif (s[i] == "Intense Treatment" or s[i] == "Keratin" or s[i] == "Hair & Make-up"):
                    add = add + 120
                else:
                    add = add + 180
            time = row1.appt_timeStart
            name1 = row1.firstStylist
            d = row1.apptDate
            t_array = (str(time)).split(':')
            hour = int(t_array[0])
            minute = int(t_array[1])
            group1.append(name1)
            group2.append("{:02d}:{:02d}".format(hour, minute))
            t = hour * 60 + minute + add
            hour, minute = divmod(t, 60)
            group3.append("{:02d}:{:02d}".format(hour, minute))
            group4.append(str(d))
    g1 = json.dumps(group1)
    g2 = json.dumps(group2)
    g3 = json.dumps(group3)   
    g4 = json.dumps(group4) 

    if request.method == 'POST':
        firstStylist = request.POST.get('stylist1')
        secondStylist = request.POST.get('stylist2')
        apptDate = request.POST.get('apptDate')
        stringTime = request.POST.get('appt_timeStart')
        arrTime = (str(stringTime)).split(':')
        h = int(arrTime[0])
        m = int(arrTime[1])
        h %= 24
        suffix = 'a' if h < 12 else 'p'
        h %= 12
        if h == 0:
            h = 12
        strTime = "{:02d}:{:02d} {}m".format(h, m, suffix)
        appt_timeStart = datetime.strptime(strTime, '%I:%M %p').time()

        create = Appointment(customer=customer,services=services,firstStylist=firstStylist,
                            secondStylist=secondStylist,apptDate=apptDate,appt_timeStart=appt_timeStart)
        create.save()
        request.session['appointment'] = "submitted"
        return redirect('clientViewAppointment')

    context = {
        'stylists':staff,
        'current_datetime':current_datetime,
        'group1': g1,
        'group2': g2,
        'group3': g3,
        'group4': g4
    }
    return render(request, 'appts_next.html', context)

def index(request):
    return render(request, 'index.html')

def appointmentsPending(request):
    current_datetime = datetime.now() 
    appointments = Appointment.objects.all()
    if "appointment" in request.session.keys():
        next = request.session['appointment']
        del request.session['appointment']
    else:
        next = None
    context = {
        'appointments':appointments,
        'next':next,
        'current_datetime':current_datetime
    }
    if request.method == 'POST':
        if request.POST['button'] == 'Reject Appointment':
            apptReject = request.POST.get('reject')
            Appointment.objects.get(pk=apptReject).delete()
            return redirect('appointmentsPending')
        elif request.POST['button'] == 'Approve Appointment':
            apptApprove = request.POST.get('approve')
            Appointment.objects.filter(pk=apptApprove).update(appointmentStatus='Approved')
        

    return render(request, 'appts_pending.html', context)

def appointmentsApproved(request):
    current_datetime = datetime.now() 
    appointments = Appointment.objects.all()

    if "appointment" in request.session.keys():
        next = request.session['appointment']
        del request.session['appointment']
    else:
        next = None
    context = {
        'appointments':appointments,
        'next':next,
        'current_datetime':current_datetime
    }
    if request.method == 'POST':
        if request.POST['button'] == 'Cancel Appointment':
            apptCancel = request.POST.get('cancel')
            Appointment.objects.filter(pk=apptCancel).update(appointmentStatus='Cancelled')
            return redirect('appointmentsApproved')
        
        elif request.POST['button'] == 'Confirm Appointment':
            id = request.POST['confirm']
            request.session['apptApproved'] = id
            # ?????
            '''request.session['date'] = str(appt.apptDate)
            request.session['time'] = str(appt.appt_timeStart)
            if appt.apptType == 'Walk In':
                request.session['name'] = appt.customer_fname + " " + appt.customer_lname
            else:
                request.session['name'] = appt.customer.customer.first_name + " " + appt.customer.customer.last_name
            request.session['services'] = appt.services
            request.session['stylists'] = appt.firstStylist + "," + appt.secondStylist'''
            # request.session['stylist1'] = appt.firstStylist
            # request.session['stylist2'] = appt.secondStylist
            return redirect('jobOrderform')
    
    return render(request, 'appts_approved.html', context) 


# CALENDAR ---------------------------------------------------------------------------------------
def calendar(request):
    current_datetime = datetime.now() 
    today = date.today()
    context = {
        'date': today,
        'current_datetime':current_datetime
    }
    return render(request, 'calendar.html', context)

def calendarDayView(request):
    a = request.POST['date']
    appointments = Appointment.objects.filter(apptDate = a)
    apptCount = Appointment.objects.filter(apptDate = a, appointmentStatus='Approved').count()
    context = {
        'a':a,
        'appointments':appointments,
        'apptCount':apptCount
    }
    
    return render(request, 'calendar_day_view.html', context)

def admincalendar(request):
    current_datetime = datetime.now() 
    today = date.today()
    context = {
        'date': today,
        'current_datetime':current_datetime
    }
    return render(request, 'admincalendar.html', context )

def admincalendardayview(request):
    current_datetime = datetime.now() 
    a = request.POST['date']
    appointments = Appointment.objects.filter(apptDate = a, appointmentStatus='Approved')
    apptCount = Appointment.objects.filter(apptDate = a, appointmentStatus='Approved').count()
    context = { 
        'a':a,
        'appointments':appointments,
        'current_datetime':current_datetime,
        'apptCount': apptCount
    }
    return render(request, 'admincalendardayview.html', context)


# WALK-IN  ---------------------------------------------------------------------------------------
def walkIn(request):
    current_datetime = datetime.now() 
    if request.method == 'POST':
        services = request.POST.getlist('services')
        request.session['fname'] = request.POST.get('fname')
        request.session['lname'] = request.POST.get('lname')
        request.session['email'] = request.POST.get('email')
        request.session['contactNumber'] = request.POST.get('contactNumber')
        request.session['services'] = services
        return redirect('walkInNext')
        
    context = {
        'current_datetime':current_datetime
    }
    return render(request, 'appts_walkin.html', context)

def walkInNext(request):
    current_datetime = datetime.now() 
    staff = Staff.objects.filter(stafftype=3)
    services = request.session['services']
    # request.session.pop('services', None)
    group1 = []
    group2 = []
    group3 = []
    group4 = []
    for row in staff:
        name = row.staff.first_name
        appt = Appointment.objects.filter(firstStylist=name)
        for row1 in appt:
            t_array=[]
            s = row1.services
            add = 0
            for i in range(0, len(s)):
                if (s[i] == "Haircut" or s[i] == "Shampoo and Blowdry" or s[i] == "Setting Ironing"):
                    add = add + 45
                elif (s[i] == "Treatment" or s[i] == "Regular Hot Oil" or s[i] == "Hair Spa" or s[i] == "Make-up"):
                    add = add + 60
                elif (s[i] == "Intense Treatment" or s[i] == "Keratin" or s[i] == "Hair & Make-up"):
                    add = add + 120
                else:
                    add = add + 180
            time = row1.appt_timeStart
            name1 = row1.firstStylist
            d = row1.apptDate
            t_array = (str(time)).split(':')
            hour = int(t_array[0])
            minute = int(t_array[1])
            group1.append(name1)
            group2.append("{:02d}:{:02d}".format(hour, minute))
            t = hour * 60 + minute + add
            hour, minute = divmod(t, 60)
            group3.append("{:02d}:{:02d}".format(hour, minute))
            group4.append(str(d))
    g1 = json.dumps(group1)
    g2 = json.dumps(group2)
    g3 = json.dumps(group3)   
    g4 = json.dumps(group4) 

    if request.method == 'POST':
        customer_fname = request.session['fname']
        # request.session.pop('fname', None)
        customer_lname = request.session['lname']
        # request.session.pop('lname', None)
        email = request.session['email']
        # request.session.pop('email', None)
        contact_num = request.session['contactNumber']
        # request.session.pop('contactNumber', None)
        firstStylist = request.POST.get('stylist1')
        secondStylist = request.POST.get('stylist2')
        apptDate = request.POST.get('apptDate')
        stringTime = request.POST.get('appt_timeStart')
        arrTime = (str(stringTime)).split(':')
        h = int(arrTime[0])
        m = int(arrTime[1])
        h %= 24
        suffix = 'a' if h < 12 else 'p'
        h %= 12
        if h == 0:
            h = 12
        strTime = "{:02d}:{:02d} {}m".format(h, m, suffix)
        appt_timeStart = datetime.strptime(strTime, '%I:%M %p').time()
        apptType = "Walk In"

        create = Appointment(customer_fname=customer_fname,customer_lname=customer_lname,email=email,contact_num=contact_num,services=services,firstStylist=firstStylist,
                            secondStylist=secondStylist,apptDate=apptDate,appt_timeStart=appt_timeStart,apptType=apptType)
        create.save()
        request.session['appointment'] = "submitted"
        return redirect('appointmentsPending')

    context = {
        'stylists':staff,
        'current_datetime':current_datetime,
        'group1': g1,
        'group2': g2,
        'group3': g3,
        'group4': g4
    }
    return render(request, 'appts_walkinnext.html', context)

# JOB ORDER AND FEEDBACK  ---------------------------------------------------------------------------------------
def jobOrderForm(request):
    current_datetime = datetime.now() 
    insalon_prods = insProduct.objects.all()
    id = request.session['apptApproved']
    appt = Appointment.objects.get(pk=id)
    # ?????
    '''date = request.session['date']
    d = datetime.strptime(date, '%Y-%m-%d')
    date = datetime.strftime(d, "%B %d, %Y")
    time = request.session['time']
    t = datetime.strptime(time, '%H:%M:%S')
    time = datetime.strftime(t, "%I:%M %p")
    name = request.session['name']
    services = request.session['services']
    stylists = request.session['stylists']'''
    # total = servicePrices 
    
    # consumed_product = request.POST.get['consumed_product']
    context = {
        'insalon_prods': insalon_prods,
        'appt':appt,
        #date': date,
        #time': time,
        #name': name,
        #services': services,
        #stylists': stylists,
        # 'stylist1':stylist1,
        # 'stylist2':stylist2,
        'current_datetime':current_datetime
    }
    if request.method == 'POST':
        prices = request.POST.getlist('price')
        servicePrices = dict(zip(appt.services, prices))
        totalPrice = request.POST.get('total')
        finalStylist = request.POST.get('stylist2')
        jobOrder = jobOrderform(appointmentInfo=appt,servicePrices=servicePrices,totalPrice=totalPrice,finalStylist=finalStylist)
        jobOrder.save()
        request.session['jobOrder'] = jobOrder.id
        appt.appointmentStatus='Confirmed'
        appt.save()
        return redirect('transactionSuccessful')
    return render(request, 'jobOrderform.html', context)

def transactionSuccessful(request):
    current_datetime = datetime.now()
    #order = jobOrderform.objects.get(pk=request.session.pop('jobOrder', None))
    order = jobOrderform.objects.get(pk=request.session['jobOrder'])
    context = {
        'current_datetime':current_datetime,
        'order':order
    }
    if request.method == 'POST':
        id = request.POST.get('Successful')
        Appointment.objects.filter(pk=id).update(appointmentStatus='Successful')
        return redirect('appointmentsApproved')
    return render(request, 'appts_transSuccessful.html', context)


def feedbackClient(request):
    current_datetime = datetime.now() 
    
    return render(request, 'feedbackClient.html')

def feedbackEditClient(request):
    current_datetime = datetime.now() 
    return render(request, 'feedbackEditClient.html')

def feedbackTable(request):
    current_datetime = datetime.now() 
    appt = Appointment.objects.filter(customer=request.user.id)
    form = jobOrderform.objects.filter(appointmentInfo__in=appt)
    fb = clientFeedback.objects.filter(feedbackInfo__in=form)
    context = {
        'current_datetime':current_datetime, 
        'form':form,
        'fb':fb,
    }
    if request.method == 'POST':
        if request.POST['button'] == 'Create Review':
            jobOrderID = request.POST.get('create')
            jobOrder = jobOrderform.objects.get(pk=jobOrderID)
            feedback = clientFeedback(feedbackInfo=jobOrder)
            feedback.save()
            return redirect('feedbackClient')
    return render(request, 'feedbackTable.html', context)

def clientViewAppointment(request):
    current_datetime = datetime.now() 
    appointments = Appointment.objects.filter(customer=request.user.id)
    if "appointment" in request.session.keys():
        next = request.session['appointment']
        del request.session['appointment']
    else:
        next = None
    context = {
        'appointments':appointments,
        'next':next,
        'current_datetime':current_datetime
    }
    if request.method == 'POST':
        #if request.POST['button'] == 'Cancel Appointment':
            apptReject = request.POST.get('cancel')
            Appointment.objects.get(pk=apptReject).delete()
            return redirect('clientViewAppointment')
    return render(request, 'clientViewAppointment.html', context)
