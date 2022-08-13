from multiprocessing import context
from tkinter import E
from unicodedata import name
from django.shortcuts import render, redirect
from .models import *

from account.models import *
from base.models import *
from account.views import *

from datetime import datetime
from datetime import date
import json
from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.core.paginator import Paginator

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum

from account.models import *

def admin_test(user):
	return user.is_staff and user.is_admin

def customer_test(user):
	return user.is_customer

def go_back(request):
	return render(request, 'access.html')

# APPOINTMENTS ----------------------------------------------------------------------------------

@login_required(login_url="/login")
@user_passes_test(customer_test, login_url="/appointments/go_back")
def appointments(request):
	current_datetime = datetime.now()
	if request.method == 'POST':
		services = request.POST.getlist('services')
		request.session['services'] = services
		return redirect('appointmentsNext')

	'''context = {
		'services_list': services_list
	}'''  
	context = {     
		'current_datetime':current_datetime,    
	}
	return render(request, 'appts.html', context)#, context)

@login_required(login_url="/login")
@user_passes_test(customer_test, login_url="/appointments/go_back")
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

	#PENDING NOTIF
	pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	#LOW STOCK NOTIF
	low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	#PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	six_months = timezone.now().date() + timedelta(days=180)
	expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	#NOTIF COUNT
	count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	notif_count = count1 + count2 + count3

	context = {
		'stylists':staff,
		'current_datetime':current_datetime,
		'group1': g1, 'group2': g2, 'group3': g3, 'group4': g4,
		'pending_count':pending_count,
		'pending_appts':pending_appts,
		'low_stock':low_stock,
		'expiring':expiring,
	}
	return render(request, 'appts_next.html', context)


def index(request):
	return render(request, 'index.html')


@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def appointmentsPending(request):
	current_datetime = datetime.now() 
	appointments = Appointment.objects.all()

	# #PENDING NOTIF
	# pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	# pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	# #LOW STOCK NOTIF
	# low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	# #PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	# six_months = timezone.now().date() + timedelta(days=180)
	# expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	# expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	# #NOTIF COUNT
	# count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	# notif_count = count1 + count2 + count3

	if "appointment" in request.session.keys():
		next = request.session['appointment']
		del request.session['appointment']
	else:
		next = None
	context = {
		'appointments':appointments,
		'next':next,
		'current_datetime':current_datetime,
	}
		# 'pending_appts': pending_appts,
		# 'pending_count': pending_count,
		# 'expiring': expiring, 
		# 'notif_count': notif_count, 
		# 'low_stock': low_stock
	if request.method == 'POST':
		if request.POST['button'] == 'Reject Appointment':
			apptReject = request.POST.get('reject')
			Appointment.objects.get(pk=apptReject).delete()
			return redirect('appointmentsPending')
		elif request.POST['button'] == 'Approve Appointment':
			apptApprove = request.POST.get('approve')
			Appointment.objects.filter(pk=apptApprove).update(appointmentStatus='Approved')
		

	return render(request, 'appts_pending.html', context)


@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def appointmentsApproved(request):
	current_datetime = datetime.now() 
	appointments = Appointment.objects.all()

	if "appointment" in request.session.keys():
		next = request.session['appointment']
		del request.session['appointment']
	else:
		next = None

	if request.method == 'POST':
		if request.POST['button'] == 'Cancel Appointment': 
			apptCancel = request.POST.get('cancel')
			Appointment.objects.filter(pk=apptCancel).update(appointmentStatus='Cancelled')
			return redirect('appointmentsApproved')
		
		elif request.POST['button'] == 'Confirm Appointment':
			apptConfirmed = request.POST.get('confirm')
			Appointment.objects.filter(pk=apptConfirmed).update(appointmentStatus='Confirmed')
			return redirect('appointmentsOngoing')
	context = {
		'appointments':appointments,
		'next':next,
		'current_datetime':current_datetime,
	}
	return render(request, 'appts_approved.html', context) 

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def appointmentsOngoing(request):
	current_datetime = datetime.now() 
	appointments = Appointment.objects.all()

	if "appointment" in request.session.keys():
		next = request.session['appointment']
		del request.session['appointment']
	else:
		next = None
	
	if request.method == 'POST':
		if request.POST['button'] == 'Cancel Appointment':
			apptCancel = request.POST.get('cancel')
			Appointment.objects.filter(pk=apptCancel).update(appointmentStatus='Cancelled')
			return redirect('appointmentsOngoing')
		elif request.POST['button'] == 'Ongoing Appointment':   
			apptOngoing = request.POST.get('ongoing')
			Appointment.objects.filter(pk=apptOngoing).update(appointmentStatus='Ongoing') 
			return redirect('alljobOrderforms')

	context = {
		'appointments':appointments,
		'next':next,
		'current_datetime':current_datetime
	}
	
	#PENDING NOTIF
	#pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	#pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	#LOW STOCK NOTIF
	#low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	#PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	#six_months = timezone.now().date() + timedelta(days=180)
	#expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	#expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	#NOTIF COUNT
	#count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	#count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	#count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	#notif_count = count1 + count2 + count3

	
	#'pending_count': pending_count,
	#'expiring': expiring, 
	#'notif_count': notif_count, 
	#'low_stock': low_stock

	#context = {
		#'current_datetime':current_datetime,
		#'pending_appts': pending_appts,	
    #}

	return render(request, 'appts_ongoing.html', context) 

# ALL SERVICES
def allservices (request):
	current_datetime = datetime.now() 

	# Hair
	hair_id = ['1', '2', '3', '4', '5']
	hair_services = Services.objects.filter(servicetype_id__in=hair_id)
	services_availed = jobOrderform.objects.all()
	all_services = []
	for row in hair_services:
		services = []
		count = 0
		total = 0
		s = row.services
		price = int(row.serviceprice) # original service price
		for row1 in services_availed:
			prices = row1.servicePrices # inputted prices per service
			if s in prices:
				count+=1
				for key, value in prices.items():
					if key == s:
						total = float(total + float(value))
		services.append(s)
		services.append(count)
		services.append(price)
		total1 = "{:.2f}".format(total)
		services.append(total1) 
		all_services.append(services) # combines them into 1 array
   
	#PENDING NOTIF
	pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	#LOW STOCK NOTIF
	low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	#PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	six_months = timezone.now().date() + timedelta(days=180)
	expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	#NOTIF COUNT
	count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	notif_count = count1 + count2 + count3
   
	context = {
		'services': all_services,
		'current_datetime': current_datetime,
		'pending_appts': pending_appts,
		'pending_count': pending_count,
		'expiring': expiring, 
		'notif_count': notif_count, 
		'low_stock': low_stock
	}
	return render(request, 'allservices.html', context)

# SERVICE LOG/ SERVICE HISTORY
def servicehistory (request):
	shistory = serviceHistory.objects.all().order_by('-dateDone')
	joborderdetails = jobOrderform.objects.all()

	#PAGE NAVIGATION
	paginator = Paginator(shistory, 10)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context = {
		'shistory': shistory, 
		'joborderdetails': joborderdetails,
		'page_prod': page_prod,
	}
	return render(request, 'servicehistory.html', context)

# JOB ORDER FORM
@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def alljobOrderforms(request):
	current_datetime = datetime.now() 
	appointments = Appointment.objects.all().order_by('apptDate', 'appt_timeStart')
	
	if "appointment" in request.session.keys():
		next = request.session['appointment']
		del request.session['appointment']
	else:
		next = None
	
	if request.method == 'POST':
		if request.POST['button'] == 'Cancel Appointment': 
			apptCancel = request.POST.get('cancel')
			Appointment.objects.filter(pk=apptCancel).update(appointmentStatus='Cancelled')
			return redirect('alljobOrderforms')
		elif request.POST['button'] == 'Proceed in Job Order Form':
			id = request.POST['jof']
			request.session['apptOngoing'] = id
			return redirect('jobOrderform')
	
	#PENDING NOTIF
	#pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	#pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	#LOW STOCK NOTIF
	#low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	#PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	#six_months = timezone.now().date() + timedelta(days=180)
	#expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	#expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	#lemuel, uso ctrl slash

	#NOTIF COUNT
	#count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	#count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	#count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	#notif_count = count1 + count2 + count3

    #2 yung context dito pwede palagay sa iisa para di magconflict
	#context = {
		#'current_datetime':current_datetime,
		#'pending_appts': pending_appts,
		#'pending_count': pending_count,
		#'expiring': expiring, 
		#'notif_count': notif_count, 
		#'low_stock': low_stock
	#}

	context = {
		'appointments':appointments,
		'next':next,
		'current_datetime':current_datetime
	}

	

	return render(request, 'alljobOrderforms.html', context)

	

# JOF V1
@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def jobOrderForm(request):
	current_datetime = datetime.now() 
	stylists = Staff.objects.filter(stafftype=3)
	id = request.session['apptOngoing'] 
	appt = Appointment.objects.get(pk=id)
	context = {
		'appt':appt,
		'stylists': stylists,
		'current_datetime':current_datetime
	}

	if request.method == 'POST':
		prices = request.POST.getlist('price')
		servicePrices = dict(zip(appt.services, prices))
		totalPrice = request.POST.get('total')
		finalStylist = request.POST.get('stylist2')
		if jobOrderform.objects.filter(appointmentInfo=appt).exists():
			jof = jobOrderform.objects.get(appointmentInfo=appt)
			jof.servicePrices = servicePrices
			jof.totalPrice = totalPrice
			jof.finalStylist = finalStylist
			jof.save()
			request.session['jobOrder'] = jof.id
		else:
			jobOrder = jobOrderform(appointmentInfo=appt,servicePrices=servicePrices,totalPrice=totalPrice,finalStylist=finalStylist)
			jobOrder.save()
			request.session['jobOrder'] = jobOrder.id
		appt.appointmentStatus='Ongoing'
		appt.save()
		return redirect('transactionSuccessful')
	
	# #PENDING NOTIF
	# pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	# pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	# #LOW STOCK NOTIF
	# low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	# #PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	# six_months = timezone.now().date() + timedelta(days=180)
	# expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	# expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	# #NOTIF COUNT
	# count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	# notif_count = count1 + count2 + count3
	
	# context = {
	# 	'current_datetime':current_datetime,
	# 	'pending_appts': pending_appts,
	# 	'pending_count': pending_count,
	# 	'expiring': expiring, 
	# 	'notif_count': notif_count, 
	# 	'low_stock': low_stock
	# }

	return render(request, 'jobOrderform.html', context)

# WALK-IN  ---------------------------------------------------------------------------------------

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
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
	
	# #PENDING NOTIF
	# pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	# pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	# #LOW STOCK NOTIF
	# low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	# #PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	# six_months = timezone.now().date() + timedelta(days=180)
	# expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	# expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	# #NOTIF COUNT
	# count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	# notif_count = count1 + count2 + count3
		
	context = {
		'current_datetime':current_datetime,
	}
	
		# 'pending_appts': pending_appts,
		# 'pending_count': pending_count,
		# 'expiring': expiring, 
		# 'notif_count': notif_count, 
		# 'low_stock': low_stock
	return render(request, 'appts_walkin.html', context)


@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def walkInNext(request):
	current_datetime = datetime.now() 
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
		customer_fname = request.session['fname']
		customer_lname = request.session['lname']
		email = request.session['email']
		contact_num = request.session['contactNumber']
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

	#PENDING NOTIF
	pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	#LOW STOCK NOTIF
	low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	#PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	six_months = timezone.now().date() + timedelta(days=180)
	expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	#NOTIF COUNT
	count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	notif_count = count1 + count2 + count3

	context = {
		'stylists':staff,
		'current_datetime':current_datetime,
		'group1': g1,
		'group2': g2,
		'group3': g3,
		'group4': g4,
		'current_datetime':current_datetime,
		'pending_appts': pending_appts,
		'pending_count': pending_count,
		'expiring': expiring, 
		'notif_count': notif_count, 
		'low_stock': low_stock
	}
	return render(request, 'appts_walkinnext.html', context)

# JOB ORDER AND FEEDBACK  ---------------------------------------------------------------------------------------

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def transactionSuccessful(request):
	current_datetime = datetime.now()
	order = jobOrderform.objects.get(pk=request.session['jobOrder'])
	context = {
		'current_datetime':current_datetime,
		'order':order
	}
	if request.method == 'POST':
		id = request.POST.get('Successful')
		Appointment.objects.filter(pk=id).update(appointmentStatus='Successful')
		return redirect('appointmentsDone')
	return render(request, 'appts_transSuccessful.html', context)


@login_required(login_url="/login")
@user_passes_test(customer_test, login_url="/appointments/go_back")
def clientViewAppointment(request):
	current_datetime = datetime.now() 
	appointments = Appointment.objects.filter(customer=request.user.id).order_by('-apptDate', '-appt_timeStart')
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
	
	# #PENDING NOTIF
	# pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	# pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	# #LOW STOCK NOTIF
	# low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	# #PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	# six_months = timezone.now().date() + timedelta(days=180)
	# expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	# expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	# #NOTIF COUNT
	# count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	# notif_count = count1 + count2 + count3

	# context = {
	# 	'current_datetime':current_datetime,
	# 	'pending_appts': pending_appts,
	# 	'pending_count': pending_count,
	# 	'expiring': expiring, 
	# 	'notif_count': notif_count, 
	# 	'low_stock': low_stock
	# }

	return render(request, 'clientViewAppointment.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def appointmentsDone(request):
	current_datetime = datetime.now() 
	appointments = Appointment.objects.all().order_by('-apptDate', '-appt_timeStart')
	#jobOrderform_timestamp = jobOrderform.objects.all()
	
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
		id = request.POST.get('Successful')
		Appointment.objects.filter(pk=id)
	
	# #PENDING NOTIF
	# pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	# pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	# #LOW STOCK NOTIF
	# low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	# #PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	# six_months = timezone.now().date() + timedelta(days=180)
	# expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	# expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	# #NOTIF COUNT
	# count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	# notif_count = count1 + count2 + count3

	# context = {
	# 	'current_datetime':current_datetime,
	# 	'pending_appts': pending_appts,
	# 	'pending_count': pending_count,
	# 	'expiring': expiring, 
	# 	'notif_count': notif_count, 
	# 	'low_stock': low_stock
	# }

	return render(request, 'appts_done.html', context)


# CALENDAR ---------------------------------------------------------------------------------------

@login_required(login_url="/login")
@user_passes_test(customer_test, login_url="/appointments/go_back")
def calendar(request):
	current_datetime = datetime.now() 
	today = date.today()
	# appointments = Appointment.objects.filter(apptDate = a)
	apptOngoingCount = Appointment.objects.filter(appointmentStatus='Ongoing').count()
	context = {
		'date': today,
		'current_datetime':current_datetime,
		'apptOngoingCount': apptOngoingCount
	}
	
	# #PENDING NOTIF
	# pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	# pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	# #LOW STOCK NOTIF
	# low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	# #PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	# six_months = timezone.now().date() + timedelta(days=180)
	# expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	# expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	# #NOTIF COUNT
	# count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	# notif_count = count1 + count2 + count3

	# context = {
	# 	'current_datetime':current_datetime,
	# 	'pending_appts': pending_appts,
	# 	'pending_count': pending_count,
	# 	'expiring': expiring, 
	# 	'notif_count': notif_count, 
	# 	'low_stock': low_stock
	# }

	return render(request, 'calendar.html', context)


@login_required(login_url="/login")
@user_passes_test(customer_test, login_url="/appointments/go_back")
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


@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def admincalendar(request):
	current_datetime = datetime.now() 
	today = date.today()
	apptOngoingCount = Appointment.objects.filter(appointmentStatus='Ongoing').count()
	context = {
		'date': today,
		'current_datetime':current_datetime,
		'apptOngoingCount': apptOngoingCount
	}

	# #PENDING NOTIF
	# pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	# pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	# #LOW STOCK NOTIF
	# low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	# #PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	# six_months = timezone.now().date() + timedelta(days=180)
	# expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	# expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	# #NOTIF COUNT
	# count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	# count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	# notif_count = count1 + count2 + count3

	# context = {
	# 	'current_datetime':current_datetime,
	# 	'pending_appts': pending_appts,
	# 	'pending_count': pending_count,
	# 	'expiring': expiring, 
	# 	'notif_count': notif_count, 
	# 	'low_stock': low_stock
	# }

	return render(request, 'admincalendar.html', context )


@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def admincalendardayview(request):
	current_datetime = datetime.now() 
	a = request.POST['date']
	appointments = Appointment.objects.filter(apptDate = a)
	apptCount = Appointment.objects.filter(apptDate = a, appointmentStatus='Approved').count()
	apptCountSucc = Appointment.objects.filter(apptDate = a, appointmentStatus='Successful').count()

	#PENDING NOTIF
	pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	#LOW STOCK NOTIF
	low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	#PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	six_months = timezone.now().date() + timedelta(days=180)
	expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	#NOTIF COUNT
	count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	notif_count = count1 + count2 + count3
	
	context = { 
		'a':a,
		'appointments':appointments,
		'current_datetime':current_datetime,
		'apptCount': apptCount,
		'apptCountSucc':apptCountSucc,
		'pending_appts': pending_appts,
		'pending_count': pending_count,
		'expiring': expiring, 
		'notif_count': notif_count, 
		'low_stock': low_stock
	}
	return render(request, 'admincalendardayview.html', context)

# ADMIN ALL SCHEDULES ---------------------------------------------------------------------------
@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def adminallschedules (request):
	current_datetime = datetime.now() 
	appointments = Appointment.objects.all().order_by('apptDate', 'appt_timeStart')
	jofs = jobOrderform.objects.all()

	pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()
	approve_count = Appointment.objects.filter(appointmentStatus='Approved').count()
	complete_count = Appointment.objects.filter(appointmentStatus='Successful').count()
	cancelled_count = Appointment.objects.filter(appointmentStatus='Cancelled').count()

	#DATE FROM TO RANGE FILTER
	if request.method == 'POST':
		if request.POST['button'] == "Search":
			fromdate=request.POST.get('fromdate')
			request.session['fromdate'] = fromdate
			todate = request.POST.get('todate')
			request.session['todate'] = todate
			appointments=Appointment.objects.filter(apptDate__gte=fromdate, apptDate__lte=todate).order_by('apptDate', 'appt_timeStart')

	#PAGE NAVIGATION
	paginator = Paginator(appointments, 5)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	#PENDING NOTIF
	pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	#LOW STOCK NOTIF
	low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	#PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	six_months = timezone.now().date() + timedelta(days=180)
	expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	#NOTIF COUNT
	count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	notif_count = count1 + count2 + count3

	context = {
		'appointments': appointments,
		'jofs': jofs,
		'page_prod': page_prod,
		'pending_count': pending_count,
		'approve_count': approve_count,
		'complete_count': complete_count,
		'cancelled_count': cancelled_count,
		'current_datetime': current_datetime,
		'pending_appts': pending_appts,
		'expiring': expiring, 
		'notif_count': notif_count, 
		'low_stock': low_stock
	}
	return render(request, 'adminallschedules.html', context)


# RATINGS & REVIEWS ---------------------------------------------------------------------------------------	
	
@login_required(login_url="/login")
@user_passes_test(customer_test, login_url="/appointments/go_back")
def feedbackTable(request):
	current_datetime = datetime.now() 
	appt = Appointment.objects.filter(customer=request.user.id).filter(appointmentStatus="Successful")
	form = jobOrderform.objects.filter(appointmentInfo__in=appt)
	fb = clientFeedback.objects.all()
	fb_list= []
	for row in fb:
		fb_list.append(row.feedbackInfo_id)
	context = {
		'current_datetime':current_datetime, 
		'form':form,
		'fb':fb,
		'fb_list':fb_list
	}
	if request.method == 'POST': 
		if request.POST['button'] == 'Create Review': 
			jobOrderID = request.POST.get('create')
			jobOrder = jobOrderform.objects.get(pk=jobOrderID)
			feedback = clientFeedback(feedbackInfo=jobOrder)
			feedback.save()
			request.session['jobOrder'] = request.POST.get('create')
			return redirect('feedbackClient')

		elif request.POST['button'] == 'Edit Review': 
			request.session['jobOrder'] = request.POST.get('edit')
			return redirect('feedbackClient')

		elif request.POST['button'] == 'View Review': 
			request.session['view'] = request.POST.get('view')
			return redirect('feedbackClientView')
	
	#PENDING NOTIF
	pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	#LOW STOCK NOTIF
	low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	#PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	six_months = timezone.now().date() + timedelta(days=180)
	expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	#NOTIF COUNT
	count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	notif_count = count1 + count2 + count3
	
	context = {
		'current_datetime':current_datetime,
		'pending_appts': pending_appts,
		'pending_count': pending_count,
		'expiring': expiring, 
		'notif_count': notif_count, 
		'low_stock': low_stock
	}

	return render(request, 'feedbacktable.html', context)
#BABALIKAN MO YEYA

@login_required(login_url="/login")
@user_passes_test(customer_test, login_url="/appointments/go_back")
def feedbackClient(request):
	current_datetime = datetime.now()
	order = jobOrderform.objects.get(pk=request.session['jobOrder'])
	feed = clientFeedback.objects.get(feedbackInfo = order)
	if request.method == 'POST':
		if request.POST['button'] == "thmbsup":
			feed.isPositive = 1
			feed.isNegative = 0
		if request.POST['button'] == "thmbsdn":
			feed.isPositive = 0
			feed.isNegative = 1
		if request.POST['button'] == "Submit":
			review = request.POST.get('comment', False)
			if review != False:
				feed.review = review
		feed.save()
		return redirect('feedbackTable')

	#PENDING NOTIF
	pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	#LOW STOCK NOTIF
	low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	#PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	six_months = timezone.now().date() + timedelta(days=180)
	expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	#NOTIF COUNT
	count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	notif_count = count1 + count2 + count3

	context = {
		'current_datetime':current_datetime,
		'order':order,
		'feed':feed,
		'pending_appts': pending_appts,
		'pending_count': pending_count,
		'expiring': expiring, 
		'notif_count': notif_count, 
		'low_stock': low_stock
	}
	return render(request, 'feedbackClient.html', context)

def feedbackClientView(request):
	current_datetime = datetime.now()
	fb = clientFeedback.objects.get(pk=request.session['view'])
	
	context = {
		'current_datetime':current_datetime,
		'fb':fb,
	}
	return render(request, 'feedbackClientView.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def adminfeedbackTable(request):
	current_datetime = datetime.now()
	form = jobOrderform.objects.filter(appointmentInfo__apptType="Online").filter(appointmentInfo__appointmentStatus="Successful").order_by('-appointmentInfo__apptDate', '-appointmentInfo__appt_timeStart')
	fb = clientFeedback.objects.all()
	fb_list= []
	for row in fb:
		fb_list.append(row.feedbackInfo_id)
	context = {
		'current_datetime':current_datetime,
		'form': form,
		'fb':fb,
		'fb_list':fb_list
	}
	if request.method == 'POST':
		request.session['reply'] = request.POST.get('reply')
		return redirect('feedbackreplyAdmin')

	#PENDING NOTIF
	pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	#LOW STOCK NOTIF
	low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	#PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	six_months = timezone.now().date() + timedelta(days=180)
	expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	#NOTIF COUNT
	count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	notif_count = count1 + count2 + count3

	context = {
		'current_datetime':current_datetime,
		'pending_appts': pending_appts,
		'pending_count': pending_count,
		'expiring': expiring, 
		'notif_count': notif_count, 
		'low_stock': low_stock
	}

	return render(request, 'adminfeedbacktable.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def feedbackreplyAdmin(request):
	current_datetime = datetime.now()
	fb = clientFeedback.objects.get(pk=request.session['reply'])
	if request.method == 'POST':
		fb.adminReply = request.POST.get('reply')
		fb.save()
		return redirect('adminfeedbackTable')

	#PENDING NOTIF
	pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	#LOW STOCK NOTIF
	low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	#PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	six_months = timezone.now().date() + timedelta(days=180)
	expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	#NOTIF COUNT
	count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	notif_count = count1 + count2 + count3	

	context = {
		'current_datetime':current_datetime,
		'fb':fb,
		'current_datetime':current_datetime,
		'pending_appts': pending_appts,
		'pending_count': pending_count,
		'expiring': expiring, 
		'notif_count': notif_count, 
		'low_stock': low_stock
	}
	return render(request, 'feedbackreplyAdmin.html', context)



# REPORT GENERATION 
@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def pdf_report_create_service_sales(request):	
	hair_id = ['1', '2', '3', '4', '5']
	hair_services = Services.objects.filter(servicetype_id__in=hair_id)
	
	services_availed = jobOrderform.objects.all()
	current_datetime = datetime.now()
	id = request.user.id
	user = CustomUser.objects.filter(pk=id)

	all_services = []
	for row in hair_services:
		services = []
		count = 0
		total = 0
		s = row.services
		price = int(row.serviceprice)
		for row1 in services_availed:
			prices = row1.servicePrices
			if s in prices:
				count+=1
				for key, value in prices.items():
					if key == s:
						total = float(total + float(value))
		services.append(s)
		services.append(count)
		services.append(price)
		total1 = "{:.2f}".format(total)
		services.append(total1)
		all_services.append(services)

	template_path = 'allservices-pdf.html' 
	context = {'services': all_services, 'current_datetime':current_datetime, 'user':user,}
	# Create a Django response object, and specify content_type as pdf 
	response = HttpResponse(content_type='application/pdf') 
	response['Content-Disposition'] =  'filename="services-sales-report.pdf"'
	# find the template and render it.

	template = get_template(template_path)  
	html = template.render(context)

	# create a pdf  
	pisa_status = pisa.CreatePDF(
	   html, dest=response)

	if pisa_status.err:
	   
	   return HttpResponse('We had some errors <pre>' + html + '</pre>')
	
	return response

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def jobOrderformtbl (request):
	current_datetime = datetime.now()
	appointments=Appointment.objects.all().order_by('apptDate', 'appt_timeStart')

	#COUNT
	form_count = Appointment.objects.filter(appointmentStatus='Successful').count
	total_price = Appointment.objects.filter(appointmentStatus='Successful').aggregate(total=Sum('joborderform__totalPrice'))

	#DATE FROM TO RANGE FILTER
	if request.method == 'POST':
		if request.POST['button'] == "Search":
			fromdate=request.POST.get('fromdate')
			request.session['fromdate'] = fromdate
			todate = request.POST.get('todate')
			request.session['todate'] = todate 
			appointments=Appointment.objects.filter(apptDate__gte=fromdate, apptDate__lte=todate).order_by('apptDate', 'appt_timeStart')

	#PENDING NOTIF
	pending_appts = Appointment.objects.filter(appointmentStatus='Pending')
	pending_count = Appointment.objects.filter(appointmentStatus='Pending').count()

	#LOW STOCK NOTIF
	low_stock = otcProduct.objects.filter(Prod_stockQty__lte=10)

	#PRODUCTS EXPIRING LESS THAN 6 MONTHS NOTIF
	six_months = timezone.now().date() + timedelta(days=180)
	expiring = otcStockHistory.objects.filter(expiry_date__lte=six_months)
	expiring = otcProduct.objects.filter(expiry_date__lte=six_months)
	
	#NOTIF COUNT
	count1 = otcStockHistory.objects.filter(expiry_date__lte=six_months).distinct().count()
	count2 = otcProduct.objects.filter(expiry_date__lte=six_months).distinct().count()
	count3 = otcProduct.objects.filter(Prod_stockQty__lte=10).count()

	notif_count = count1 + count2 + count3
	
	context = {
		'current_datetime':current_datetime,
		'appointments':appointments,
		'form_count':form_count,
		'total_price': total_price,
		'pending_appts': pending_appts,
		'pending_count': pending_count,
		'expiring': expiring, 
		'notif_count': notif_count, 
		'low_stock': low_stock
	}
	#'form_amount':form_amount
	return render(request, 'jobOrderformtbl.html', context)

# JOB ORDER FORMS REPORT
@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def jobOrderformtblreport (request):
	appointments=Appointment.objects.all().order_by('apptDate', 'appt_timeStart')
	jofs = jobOrderform.objects.all()
	current_datetime = datetime.now()

	id = request.user.id
	user = CustomUser.objects.filter(pk=id)
   
	#yung table na yun bago ahhh di na yung tbl sa html
	
	#fromdate = request.session['fromdate']
	#todate = request.session['todate']
	if "fromdate" in request.session.keys():
		fromdate = request.session['fromdate']
		del request.session['fromdate']
	else:
		fromdate = "2000-01-01"

	if "todate" in request.session.keys():
		todate = request.session['todate']
		del request.session['todate']
	else:
		todate = "2050-01-01"
	

	# FOR GETTING TOTAL CUSTOMERS
	online_count = Appointment.objects.filter(apptType='Online', appointmentStatus='Successful').distinct().count()
	walkin_count = Appointment.objects.filter(apptType='Walk In', appointmentStatus='Successful').distinct().count()
	cust_count = walkin_count + online_count

	# FOR GETTING TOTAL STORE EARNINGS
	total_earnings = Appointment.objects.filter(appointmentStatus='Successful').aggregate(total=Sum('joborderform__totalPrice'))

	# GET EARLIEST AND LATEST DATE 
	#earlydate =  Appointment.objects.filter(apptDate__gte=fromdate, apptDate__lte=todate).first()
	earlydate =  Appointment.objects.filter(apptDate__gte=fromdate, apptDate__lte=todate).order_by('apptDate').first()
	
	#latedate =  Appointment.objects.filter(apptDate__gte=fromdate, apptDate__lte=todate).last()
	latedate =  Appointment.objects.filter(apptDate__gte=fromdate, apptDate__lte=todate).order_by('apptDate').last()

	# FOR GETTING TOTAL SERVICES DONE
	appointments=Appointment.objects.filter(apptDate__gte=fromdate, apptDate__lte=todate).order_by('apptDate', 'appt_timeStart')

	total_services = 0
	for row in appointments:
		if row.appointmentStatus == "Successful":
			c = len(row.services)
			total_services = total_services + c
	

	template_path = 'jobOrderformtable-pdf.html' 
	context = {'appointments':appointments,
				'jofs':jofs, 
				'current_datetime':current_datetime, 
				'total_services':total_services,
				'total_earnings': total_earnings,
				'online_count':online_count, 
				'walkin_count':walkin_count, 
				'cust_count':cust_count, 'fromdate':fromdate, 
				'todate':todate, 
				'user': user,
				'earlydate': earlydate,
				'latedate': latedate,
			}
	
	#Create a Django response object, and specify content_type as pdf 
	response = HttpResponse(content_type='application/pdf') 
	response['Content-Disposition'] =  'filename="jof-sales-report.pdf"'
	#find the template and render it.

	template = get_template(template_path)  
	html = template.render(context)

	# create a pdf   
	pisa_status = pisa.CreatePDF(
		html, dest=response)

	if pisa_status.err:
	   
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	
	return response	


# ADMIN - ALL SCHEDULES REPORT ---------------------------------------------------------------------------------------------------
@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def adminallschedulesreport (request):
	appointments=Appointment.objects.all().order_by('apptDate', 'appt_timeStart')
	jofs = jobOrderform.objects.all()
	current_datetime = datetime.now()
	id = request.user.id
	user = CustomUser.objects.filter(pk=id)

	if "fromdate" in request.session.keys():
		fromdate = request.session['fromdate']
		del request.session['fromdate']
	else:
		fromdate = "2000-01-01"
	
	if "todate" in request.session.keys():
		todate = request.session['todate']
		del request.session['todate']
	else:
		todate = "2050-01-01"

	# GET EARLIEST AND LATEST DATE 
	earlydate =  Appointment.objects.filter(apptDate__gte=fromdate, apptDate__lte=todate).order_by('apptDate').first()
	latedate =  Appointment.objects.filter(apptDate__gte=fromdate, apptDate__lte=todate).order_by('apptDate').last()
	

	# FOR GETTING TOTAL CUSTOMERS
	online_count = Appointment.objects.filter(apptType='Online',apptDate__gte=fromdate, apptDate__lte=todate).distinct().count()
	walkin_count = Appointment.objects.filter(apptType='Walk In' ,apptDate__gte=fromdate, apptDate__lte=todate).distinct().count()
	

	
	# APPOINTMENT COUNT
	pending_count = Appointment.objects.filter(appointmentStatus='Pending',apptDate__gte=fromdate, apptDate__lte=todate).count()
	approve_count = Appointment.objects.filter(appointmentStatus='Approved',apptDate__gte=fromdate, apptDate__lte=todate).count()
	complete_count = Appointment.objects.filter(appointmentStatus='Successful',apptDate__gte=fromdate, apptDate__lte=todate).count()
	cancelled_count = Appointment.objects.filter(appointmentStatus='Cancelled',apptDate__gte=fromdate, apptDate__lte=todate).count()

	appointment_count = pending_count + approve_count + complete_count + cancelled_count

	appointments=Appointment.objects.filter(apptDate__gte=fromdate, apptDate__lte=todate).order_by('apptDate', 'appt_timeStart')

	template_path = 'adminallschedules-pdf.html' 
	context = {
				'current_datetime':current_datetime,
				'appointments': appointments,
				'jofs': jofs,
				'pending_count': pending_count,
				'approve_count': approve_count,
				'complete_count': complete_count,
				'cancelled_count': cancelled_count,
				'appointment_count': appointment_count,
				'online_count': online_count,
				'walkin_count': walkin_count,
				'fromdate':fromdate,
				'todate':todate,
				'user': user,
				'earlydate': earlydate,
				'latedate': latedate,
			}
	
	#Create a Django response object, and specify content_type as pdf 
	response = HttpResponse(content_type='application/pdf') 
	response['Content-Disposition'] =  'filename="all-schdedules-report.pdf"'
	#find the template and render it.

	template = get_template(template_path)  
	html = template.render(context)

	# create a pdf  
	pisa_status = pisa.CreatePDF(
		html, dest=response)

	if pisa_status.err:
	   
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	
	return response	
	

# JOB ORDER FORM REPORT -------------------------------------------------------------------------------------------------------
@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/appointments/go_back")
def jobOrderFormreport(request):
	id = request.user.id
	user = CustomUser.objects.filter(pk=id)
	order = jobOrderform.objects.get(pk=request.session['jobOrder'])
	current_datetime = datetime.now()
	if request.method == 'POST':
		id = request.POST.get('Successful')
		Appointment.objects.filter(pk=id).update(appointmentStatus='Successful')

	template_path = 'jobOrderform-pdf.html' 
	context = {'order':order, 'current_datetime':current_datetime, 'user':user, }
	
	response = HttpResponse(content_type='application/pdf') 
	response['Content-Disposition'] =  'filename="Job-order-form.pdf"'

	template = get_template(template_path)  
	html = template.render(context)

	pisa_status = pisa.CreatePDF(
		html, dest=response)

	if pisa_status.err:
	   
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	
	return response	
