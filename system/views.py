from multiprocessing import context
from tkinter import E
from unicodedata import name
from django.shortcuts import render, redirect
from .models import *

from account.models import *

from datetime import datetime
from datetime import date

def home(request):
    return render(request, 'home.html')

# APPOINTMENTS ----------------------------------------------------------------------------------
def appointments(request):
    #services_list = Services.objects.filter(servicetype_id__in=[1,2,3,4,5])
    # services in database
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
    return render(request, 'appts.html')#, context)


def appointmentsNext(request):
    customer = Customer.objects.get(customer=request.user)
    staff = Staff.objects.filter(stafftype=3)
    services = request.session['services']
    if (services == '["Haircut"]' or services == '["Shampoo and Blowdry"]' or services == '["Setting/Ironing"]'):
        add = 45 * 60 * 1000
    elif (services == '["Treatment"]' or services == '["Regular Hot Oil"]' or services == '["Hair Spa"]' or services == '["Make-up"]'):
        add = 60 * 60 * 1000
    elif (services == '["Intense Treatment"]' or services == '["Keratin"]' or services == '["Hair & Make-up"]'):
        add = 120 * 60 * 1000
    else:
        add = 180 * 60 * 1000
    group1 = []
    group2 = []
    group3 = []
    for row in staff:
        name = row.staff.first_name
        appt = Appointment.objects.filter(firstStylist=name)
        times = []
        for row1 in appt:
            time = row1.appt_timeStart
            t_array = (str(time)).split(':')
            hour = int(t_array[0])
            minute = int(t_array[1])
            hour = hour * 3600
            minute = minute * 60 * 1000
            total = hour + minute
            group3.append(total)
            times.append(time)
        group1.append(name)
        group2.append(times)
        count1 = len(group1)
        count2 = len(group2)

    if request.method == 'POST':
        firstStylist = request.POST.get('stylist1')
        secondStylist = request.POST.get('stylist2')
        apptDate = request.POST.get('apptDate')
        stringTime = request.POST.get('appt_timeStart')
        appt_timeStart = datetime.strptime(stringTime, '%I:%M %p').time()
        apptType = "Online"

        create = Appointment(customer=customer,services=services,firstStylist=firstStylist,
                            secondStylist=secondStylist,apptDate=apptDate,appt_timeStart=appt_timeStart)
        create.save()
        request.session['appointment'] = "submitted"
        return redirect('clientViewAppointment')

    context = {
        'stylists':staff,
        'add':add,
        'group1':group1,
        'group2':group2,
        'group3':group3,
        'count1':count1,
        'count2':count2
    }
    return render(request, 'appts_next.html', context)

def index(request):
    return render(request, 'index.html')

def appointmentsPending(request):
    appointments = Appointment.objects.all()
    if "appointment" in request.session.keys():
        next = request.session['appointment']
        del request.session['appointment']
    else:
        next = None
    context = {
        'appointments':appointments,
        'next':next
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
    appointments = Appointment.objects.all()

    if "appointment" in request.session.keys():
        next = request.session['appointment']
        del request.session['appointment']
    else:
        next = None
    context = {
        'appointments':appointments,
        'next':next
    }
    if request.method == 'POST':
        if request.POST['button'] == 'Cancel Appointment':
            apptCancel = request.POST.get('cancel')
            Appointment.objects.filter(pk=apptCancel).update(appointmentStatus='Cancelled')
            return redirect('appointmentsApproved')
        
        elif request.POST['button'] == 'Confirm Appointment':
            id = request.POST['confirm']
            appt=Appointment.objects.get(pk=id)
            request.session['date'] = str(appt.apptDate)
            request.session['time'] = str(appt.appt_timeStart)
            request.session['name'] = appt.customer_fname + " " + appt.customer_lname 
            request.session['services'] = appt.services
            request.session['stylists'] = appt.firstStylist + "," + appt.secondStylist
            return redirect('jobOrderform')
    
    return render(request, 'appts_approved.html', context) 

def transactionSuccessful(request):
    return render(request, 'appts_transSuccessful.html')
# CALENDAR ---------------------------------------------------------------------------------------
def calendar(request):
    today = date.today()
    return render(request, 'calendar.html', {'date': today} )

def calendarDayView(request):
    a = request.POST['date']
    appointments = Appointment.objects.filter(apptDate = a)
    context = {
        'appointments':appointments
    }
    return render(request, 'calendar_day_view.html', context)


# WALK-IN  ---------------------------------------------------------------------------------------
def walkIn(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        services = request.POST.getlist('services')
        request.session['fname'] = fname
        request.session['lname'] = lname
        request.session['services'] = services
        return redirect('walkInNext')
    return render(request, 'appts_walkin.html')

def walkInNext(request):
    staff = Staff.objects.filter(stafftype=3)
    services = request.session['services']
    if (services == '["Haircut"]' or services == '["Shampoo and Blowdry"]' or services == '["Setting/Ironing"]'):
        add = 45 * 60 * 1000
    elif (services == '["Treatment"]' or services == '["Regular Hot Oil"]' or services == '["Hair Spa"]' or services == '["Make-up"]'):
        add = 60 * 60 * 1000
    elif (services == '["Intense Treatment"]' or services == '["Keratin"]' or services == '["Hair & Make-up"]'):
        add = 120 * 60 * 1000
    else:
        add = 180 * 60 * 1000
    group1 = []
    group2 = []
    group3 = []
    for row in staff:
        name = row.staff.first_name
        appt = Appointment.objects.filter(firstStylist=name)
        times = []
        for row1 in appt:
            time = row1.appt_timeStart
            t_array = (str(time)).split(':')
            hour = int(t_array[0])
            minute = int(t_array[1])
            hour = hour * 3600
            minute = minute * 60 * 1000
            total = hour + minute
            group3.append(total)
            times.append(time)
        group1.append(name)
        group2.append(times)
        count1 = len(group1)
        count2 = len(group2)

    if request.method == 'POST':
        customer_fname = request.session['fname']
        customer_lname = request.session['lname']
        firstStylist = request.POST.get('stylist1')
        secondStylist = request.POST.get('stylist2')
        apptDate = request.POST.get('apptDate')
        stringTime = request.POST.get('appt_timeStart')
        appt_timeStart = datetime.strptime(stringTime, '%I:%M %p').time()
        apptType = "Walk In"

        create = Appointment(customer_fname=customer_fname,customer_lname=customer_lname,services=services,firstStylist=firstStylist,
                            secondStylist=secondStylist,apptDate=apptDate,appt_timeStart=appt_timeStart,apptType=apptType)
        create.save()
        request.session['appointment'] = "submitted"
        return redirect('appointmentsPending')

    context = {
        'stylists':staff,
        'add':add,
        'group1':group1,
        'group2':group2,
        'group3':group3,
        'count1':count1,
        'count2':count2
    }
    return render(request, 'appts_walkinnext.html', context)

# JOB ORDER AND FEEDBACK  ---------------------------------------------------------------------------------------
def jobOrderform(request):
    date = request.session['date']
    d = datetime.strptime(date, '%Y-%m-%d')
    date = datetime.strftime(d, "%B %d, %Y")
    time = request.session['time']
    t = datetime.strptime(time, '%H:%M:%S')
    time = datetime.strftime(t, "%I:%M %p")
    name = request.session['name']
    services = request.session['services']
    stylists = request.session['stylists']
    context = {
        'date': date,
        'time': time,
        'name': name,
        'services': services,
        'stylists': stylists,
    }

    return render(request, 'jobOrderform.html', context)

def feedbackClient(request):
    return render(request, 'feedbackClient.html')

def feedbackEditClient(request):
    return render(request, 'feedbackEditClient.html')

def clientViewAppointment(request):
    appointments = Appointment.objects.filter(customer=request.user.id)
    if "appointment" in request.session.keys():
        next = request.session['appointment']
        del request.session['appointment']
    else:
        next = None
    context = {
        'appointments':appointments,
        'next':next
    }
    if request.method == 'POST':
        #if request.POST['button'] == 'Cancel Appointment':
            apptReject = request.POST.get('cancel')
            Appointment.objects.get(pk=apptReject).delete()
            return redirect('clientViewAppointment')
    return render(request, 'clientViewAppointment.html', context)

def admincalendar(request):
    return render(request, 'admincalendar.html')


