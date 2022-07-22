from multiprocessing import context
from django.shortcuts import render, redirect
from .models import *
from datetime import datetime

def home(request):
    return render(request, 'home.html')

def appointments(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        services = request.POST.getlist('services')
        request.session['fname'] = fname
        request.session['lname'] = lname
        request.session['services'] = services
        return redirect('appointmentsNext')
    return render(request, 'appts.html')

def appointmentsNext(request):
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

        create = Appointment(customer_fname=customer_fname,customer_lname=customer_lname,services=services,firstStylist=firstStylist,
                            secondStylist=secondStylist,apptDate=apptDate,appt_timeStart=appt_timeStart)
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
    return render(request, 'appts_next.html', context)

def index(request):
    return render(request, 'index.html')

# CALENDAR
def calendar(request):

    return render(request, 'calendar.html' )

def calendarDayView(request):
    a = request.POST['date']
    appointments = Appointment.objects.filter(apptDate = a)
    context = {
        'appointments':appointments
    }
    return render(request, 'calendar_day_view.html', context)

# APPOINTMENTS
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
    context = {
        'appointments':appointments
    }
    return render(request, 'appts_approved.html', context)

def jobOrderform(request):
    return render(request, 'jobOrderform.html')


