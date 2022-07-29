from django.shortcuts import redirect, render
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.urls import reverse

import json
import datetime
from datetime import datetime
from django.contrib import messages

from .models import * 
from .forms import otcProductForm, insProductForm, IssueForm, ReceiveForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
User = settings.AUTH_USER_MODEL


# Create your views here.

#def home(request):
	#return render(request, 'base/home.html')

# OTC PRODUCTS ------------------------------------------------------
def shop(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items=[]
		order =  {'get_cart_total':0, 'get_cart_items':0, 'pickup': False}
		cartItems = order['get_cart_items']

	q = request.GET.get('q') if request.GET.get('q') != None else ''
	products = otcProduct.active_objects.filter(
		Q(ProdType_Name__ProdType_Name__icontains=q) |
		Q(Cat_Name__Cat_Name__icontains=q) |
		Q(Prod_Name__icontains=q) 
	).order_by('-date_created')

	#CATEGORIES
	prod_type = ProductType.objects.all()
	categories = Category.objects.all()

	#PAGE NAVIGATION
	paginator = Paginator(products, 9)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context= {'prod_type': prod_type, 'categories': categories, 'products': products, 'page_prod': page_prod, 'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'base/otc-products/client/shop.html', context)

def shopIndivProduct(request, pk):
	product = otcProduct.active_objects.get(id=pk)

	#BROWSE OTHER PRODUCTS
	browse = otcProduct.active_objects.filter(
		Q(Cat_Name=product.Cat_Name) |
		Q(ProdType_Name=product.ProdType_Name)
	).order_by('?').exclude(id=pk)

	context = {'product': product, 'browse': browse}
	return render(request, 'base/otc-products/client/shop_indiv_product.html', context)


@login_required(login_url="/login")
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

#DEDUCT FROM STOCK
@login_required(login_url="/login")
def deduct_items(request, pk):
	product = otcProduct.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=product)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.Prod_stockQty -= instance.deduct_stock
		messages.success(request, "Deducted from Inventory. " + str(instance.Prod_stockQty) + " " + str(instance.Prod_Name) + "s now left in stock.")
		instance.save()

		deduct_history = otcStockHistory(
			Prod_Name = instance.Prod_Name,
			Prod_stockQty = instance.Prod_stockQty,
			deduct_stock = instance.deduct_stock,
			last_updated = instance.last_updated
			)
		deduct_history.save()
		
		return redirect('/shop/otc/products/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": 'Issue ' + str(product.Prod_Name),
		"form": form,
		"product": product,
		"username": 'Issue By: ' + str(request.user),
	}
	return render(request, "base/otc-products/admin/use-stock.html", context)


#RESTOCK 
@login_required(login_url="/login")
def add_items(request, pk):
	product = otcProduct.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=product)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.Prod_stockQty += instance.add_stock
		instance.expiry_date
		instance.save()
		messages.success(request, "Restocked Inventory. " + str(instance.Prod_stockQty) + " " + str(instance.Prod_Name)+"s now in stock.")
		
		restock_history = otcStockHistory(
			Prod_Name = instance.Prod_Name,
			Prod_stockQty = instance.Prod_stockQty,
			add_stock = instance.add_stock,
			expiry_date = instance.expiry_date,
			last_updated = instance.last_updated
			)
		restock_history.save()

		return redirect('/shop/otc/products/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			'title': 'Receive ' + str(product.Prod_Name),
			'instance': product,
			'form': form
		}
	return render(request, "base/otc-products/admin/add-stock.html", context)

		
#HISTORY
@login_required(login_url="/login")
def otc_history(request):
	history = otcStockHistory.objects.all().order_by('-last_updated')

	#PAGE NAVIGATION
	paginator = Paginator(history, 10)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context = {'history': history, 'page_prod': page_prod}
	return render(request, "base/otc-products/admin/otc-history.html",context)

@login_required(login_url="/login")
def otc_indivProduct(request, pk):
	product = otcProduct.objects.get(id=pk)

	context = {'product': product}
	return render(request, 'base/otc-products/admin/indiv_product.html', context)

@login_required(login_url="/login")
def otc_createProduct(request):
	form = otcProductForm()
	if request.method == 'POST':
		form = otcProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('otc-products')

	context = {'form': form}
	return render(request, 'base/otc-products/admin/product_form.html', context)


@login_required(login_url="/login")
def otc_updateProduct(request, pk):
	product = otcProduct.objects.get(id=pk)
	form = otcProductForm(instance=product)

	if request.method == 'POST':
		form = otcProductForm(request.POST, request.FILES, instance=product)
		if form.is_valid():
			form.save()
			return redirect('otc-products')

	context = {'form': form}
	return render(request, 'base/otc-products/admin/product_form.html', context)

#def deleteProduct(request, pk):
#    product = otcProduct.objects.get(id=pk)
#    if request.method == 'POST':
#        product.delete()
#        return redirect('products')

#    return render(request, 'base/delete_product.html', {'obj': product})


# INSALON PRODUCTS ------------------------------------------------------
@login_required(login_url="/login")
def insProducts(request):
	current_datetime = datetime.now()
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	products = insProduct.objects.all()
	
	search = insProduct.objects.filter(
		Q(id__icontains=q) |
		Q(Prod_Name__icontains=q) |
		Q(ProdType_Name__ProdType_Name__icontains=q) |
		Q(Cat_Name__Cat_Name__icontains=q) 
	).order_by('-date_created')
	
	#PAGE NAVIGATION
	paginator = Paginator(search, 10)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context = {'products': products, 'search': search, 'page_prod': page_prod,'current_datetime':current_datetime,}
	return render(request, 'base/ins-products/products.html', context)


@login_required(login_url="/login")
def ins_indivProduct(request, pk):
	product = insProduct.objects.get(id=pk)

	context = {'product': product}
	return render(request, 'base/ins-products/indiv_product.html', context)

@login_required(login_url="/login")
def ins_createProduct(request):
	form = insProductForm()
	if request.method == 'POST':
		form = insProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('ins-products')

	context = {'form': form}
	return render(request, 'base/ins-products/product_form.html', context)


@login_required(login_url="/login")
def ins_updateProduct(request, pk):
	product = insProduct.objects.get(id=pk)
	form = insProductForm(instance=product)

	if request.method == 'POST':
		form = insProductForm(request.POST, request.FILES, instance=product)
		if form.is_valid():
			form.save()
			return redirect('ins-products')

	context = {'form': form}
	return render(request, 'base/ins-products/product_form.html', context)

#  ------------------------------------------------------

#CART RENDER VIEW
@login_required(login_url="/login")
def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items=[]
		order =  {'get_cart_total':0, 'get_cart_items':0, 'pickup': False}
		cartItems = order['get_cart_items']
		
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'base/otc-products/client/cart.html', context)

#CHECKOUT RENDER VIEW
@login_required(login_url="/login")
def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items=[]
		order =  {'get_cart_total':0, 'get_cart_items':0, 'pickup': False}
		cartItems = order['get_cart_items']
		
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'base/otc-products/client/checkout.html', context)

#PURCHASES RENDER VIEW
@login_required(login_url="/login")
def my_purchases(request):
	customer = request.user.customer
	items = OrderItem.objects.filter(order__customer=customer, order__complete=True)
	orders = OrderPickUp.objects.filter(order__customer=customer, order__complete=True).order_by('-order__date_ordered')
	

	#PAGE NAVIGATION
	paginator = Paginator(orders, 5)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context = {'items':items, 'orders':orders, 'page_prod': page_prod}
	return render(request, 'base/otc-products/my-purchases.html', context)

#UPDATE ITEM RENDER VIEW
@login_required(login_url="/login")
def updateItem(request):
	## parse since it is a string value
	data = json.loads(request.body)
	## get the product id and action
	productId = data['productId']
	action = data['action']

	print('Action:', action)
	print('Product ID:', productId)

	## query customer
	customer = request.user.customer
	## get the product we are passing in
	product = otcProduct.objects.get(id=productId)
	## create or add to order
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	## quantity
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

@login_required(login_url="/login")
def processOrder(request):
	transaction_id = datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.pickup == True:
		OrderPickUp.objects.create(
		customer=customer,
		order=order,
		pickup=data['pickup']['pickupdate'],
		)

	return JsonResponse('Order Complete!', safe=False)

#ADMIN VIEW: PENDING ORDERS
@login_required(login_url="/login")
def pending_orders(request):
	items = OrderItem.objects.all()

	if request.method == 'POST':
		if request.POST['button'] == 'Reject':
			reject_pickup = request.POST.get('reject')
			Order.objects.filter(pk=reject_pickup).update(pickupstat_id='Cancelled')
		elif request.POST['button'] == 'Approve':
			approve_pickup = request.POST.get('approve')
			Order.objects.filter(pk=approve_pickup).update(pickupstat_id='Approved')
	
	#SEARCH -- MIGHT CHANGE LATER
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	reservations = OrderPickUp.objects.filter(order__complete=True, order__pickupstat_id='Pending')
	orders = OrderPickUp.objects.filter(
		Q(order__transaction_id__icontains=q) |
		Q(pickup__icontains=q) 
	)

	#PAGE NAVIGATION
	paginator = Paginator(reservations, 5)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context = {'orders': orders, 'items': items, 'page_prod': page_prod}
	return render(request, 'base/otc-products/admin/pending-reservations.html', context)

#ADMIN VIEW: ORDER ITEMS OF INDIVIDUAL CUSTOMERS

@login_required(login_url="/login")
def order_items(request, pk):
	order = Order.objects.get(id=pk)
	orderitems = OrderItem.objects.filter(order=order).order_by('-id')

	context = {'order': order, 'orderitems': orderitems}
	return render(request, 'base/otc-products/admin/order-details.html', context)

#ADMIN VIEW: APPROVAL OF ORDERS
@login_required(login_url="/login")
def approved_orders(request):
	current_datetime = datetime.now()
	items = OrderItem.objects.all()

	if request.method == 'POST':
		if request.POST['button'] == 'Cancel':
			cancel_pickup = request.POST.get('cancel')
			Order.objects.filter(pk=cancel_pickup).update(pickupstat_id='Cancelled')
		elif request.POST['button'] == 'Receive Payment':
			transac_successful = request.POST.get('transaction-successful')
			Order.objects.filter(pk=transac_successful).update(pickupstat_id='Transaction Successful')
			return HttpResponseRedirect(reverse('sales-invoice', args=[str(transac_successful)]))
			

	#SEARCH -- MIGHT CHANGE LATER
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	reservations = OrderPickUp.objects.filter(order__complete=True, order__pickupstat_id='Approved')
	orders = OrderPickUp.objects.filter(
		Q(order__transaction_id__icontains=q) |
		Q(pickup__icontains=q) 
	)

	#Q(order__customer__name_icontains=q) |

	#PAGE NAVIGATION
	paginator = Paginator(reservations, 5)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context = {'orders': orders, 'items': items, 'page_prod': page_prod, 'current_datetime':current_datetime,  }
	return render(request, 'base/otc-products/admin/approved-reservations.html', context)

#SALES INVOICE RENDER VIEW

@login_required(login_url="/login")
def salesinvoice(request, pk):
	items = OrderItem.objects.all()
	invoice = OrderPickUp.objects.get(order__id=pk)
	#name = Order.objects.get(id=invoice.product_pickupID.id)
	#invoices = OrderPickUp.objects.all() 'invoices': invoices

	if request.method =='POST':
		if request.POST['button'] == 'Confirm':
	#       kunin yung quantity nung inorder
	#       sa table na may product stock, kunin din yung quantity
	#       nakauha mo na both diba, dun mo na minus yung quantity at stock
	#       tsaka siya ise-save 
	#       
			itemquanti = OrderItem.objects.filter(order=invoice.order.id)
			#products = otcProduct.objects.all()

			for p in itemquanti:
				prod = otcProduct.objects.get(id=p.product.id)
				proddiff = prod.Prod_stockQty - p.quantity  
				prod.Prod_stockQty = proddiff
				prod.save()

				restock_history = otcStockHistory(
				Prod_Name = prod.Prod_Name,
				Prod_stockQty = prod.Prod_stockQty,
				deduct_stock = p.quantity,
				last_updated = prod.last_updated
				)
				restock_history.save()
			return redirect('approved-reservations')
	#        
	context = {'invoice': invoice, 'items': items}
	return render(request, 'base/otc-products/admin/sales-invoice.html', context)