from multiprocessing import context
from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from datetime import datetime


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
    if request.method == 'POST':
        customer_fname = request.session['fname']
        customer_lname = request.session['lname']
        services = request.session['services']
        firstStylist = request.POST.get('stylist1')
        secondStylist = request.POST.get('stylist2')
        apptDate = request.POST.get('apptDate')
        stringTime = request.POST.get('appt_timeStart')
        appt_timeStart = datetime.strptime(stringTime, '%I:%M %p').time()
        create = Appointment(customer_fname=customer_fname,customer_lname=customer_lname,services=services,firstStylist=firstStylist,
                            secondStylist=secondStylist,apptDate=apptDate,appt_timeStart=appt_timeStart)
        create.save()
        return HttpResponse("Appointment is now pending. Wait for few minutes for the admin's approval.")
    return render(request, 'appts_next.html')



def index(request):
    return render(request, 'index.html')

def calendar(request):
    return render(request, 'calendar.html')

def appointmentsPending(request):
    appointments = Appointment.objects.all()
    context = {
        'appointments':appointments  
    }
    if request.method == 'POST':
        if request.POST['button'] == 'Reject Appointment':
            apptReject = request.POST.get('reject')
            Appointment.objects.get(pk=apptReject).delete()
            return redirect('appointmentsPending')
        else:
            apptReject = request.POST.get('accept')
            return redirect('appointmentsPending')
    return render(request, 'appts_pending.html', context)
