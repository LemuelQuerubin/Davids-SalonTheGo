from system.models import *
from system.views import *
from base.models import *
from base.views import *


#views ng mga ididisplay n

# adminpanel


# APPOINTMENTS PENDING
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


# PRODUCTS - LOW IN STOCK
def otcProducts(request):
	current_datetime = datetime.now()
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	products = otcProduct.objects.all()
	
	
	search = otcProduct.objects.filter(
		Q(id__icontains=q) |
		Q(Prod_Name__icontains=q) |
		Q(ProdType_Name__ProdType_Name__icontains=q) |
		Q(Cat_Name__Cat_Name__icontains=q) 
	).order_by('-date_created')
	
	#form = StatusForm()
	#if request.method == 'POST':
	#    form = StatusForm(request.POST)
	#    if form.is_valid():
	#        form.save()

	#PAGE NAVIGATION
	paginator = Paginator(search, 10)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context = {'products': products, 'search': search, 'page_prod': page_prod,'current_datetime':current_datetime,  }
	return render(request, 'base/otc-products/admin/products.html', context)