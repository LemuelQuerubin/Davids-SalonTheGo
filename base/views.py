from django.shortcuts import redirect, render
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.urls import reverse

import json
import datetime
from datetime import datetime
from django.contrib import messages
from django.db.models import Sum, F, FloatField

from .models import * 
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
User = settings.AUTH_USER_MODEL

from django.template.loader import get_template
from django.db.models import Count
from xhtml2pdf import pisa


# Create your views here.

#def home(request):
	#return render(request, 'base/home.html')

def admin_test(user):
	return user.is_staff and user.is_admin

def customer_test(user):
	return user.is_customer

def go_back(request):
	
	return render(request, 'access.html')

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
	reviews = CustomerReview.objects.filter(product=product)

	#BROWSE OTHER PRODUCTS
	browse = otcProduct.active_objects.filter(
		Q(Cat_Name=product.Cat_Name) |
		Q(ProdType_Name=product.ProdType_Name)
	).order_by('?').exclude(id=pk)

	#PAGE NAVIGATION
	paginator = Paginator(reviews, 5)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context = {'product': product, 'browse': browse, 'reviews': reviews, 'page_prod': page_prod}
	return render(request, 'base/otc-products/client/shop_indiv_product.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/shop/otc/products/go_back")
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
@user_passes_test(admin_test, login_url="/shop/otc/products/go_back")
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
@user_passes_test(admin_test, login_url="/shop/otc/products/go_back")
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
@user_passes_test(admin_test, login_url="/shop/otc/history/go_back")
def otc_history(request):
	history = otcStockHistory.objects.all().order_by('-last_updated')
	#history = otcStockHistory.objects.filter(Prod_Name = 'Insight Rebalancing Shampoo').order_by('-last_updated')

	#PAGE NAVIGATION
	paginator = Paginator(history, 10)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context = {'history': history, 'page_prod': page_prod}
	return render(request, "base/otc-products/admin/otc-history.html",context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/shop/otc/products/go_back")
def otc_indivProduct(request, pk):
	product = otcProduct.objects.get(id=pk)
	history = otcStockHistory.objects.filter(Prod_Name=product).order_by('-last_updated')

	context = {'product': product, 'history': history}
	return render(request, 'base/otc-products/admin/indiv_product.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/shop/otc/products/go_back")
def otc_indivProductHistory(request, pk):
	product = otcProduct.objects.get(id=pk)
	history = otcStockHistory.objects.filter(Prod_Name=product).order_by('-last_updated')

	context = {'product': product, 'history': history}
	return render(request, 'base/otc-products/admin/indiv_product_history.html', context)


@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/shop/otc/products/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
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
@user_passes_test(admin_test, login_url="/shop/otc/products/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
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
@user_passes_test(admin_test, login_url="/shop/ins/products/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
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
@user_passes_test(admin_test, login_url="/shop/ins/products/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
def ins_indivProduct(request, pk):
	product = insProduct.objects.get(id=pk)

	context = {'product': product}
	return render(request, 'base/ins-products/indiv_product.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/shop/ins/products/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
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
@user_passes_test(admin_test, login_url="/shop/ins/products/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
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
@user_passes_test(customer_test, login_url="/shop/cart/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
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
@user_passes_test(customer_test, login_url="/shop/checkout/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
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
@user_passes_test(customer_test, login_url="/shop/my-purchases/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
def my_purchases(request):
	current_datetime = datetime.now()
	customer = request.user.customer
	items = OrderItem.objects.filter(order__customer=customer, order__complete=True)
	
	if request.method == 'POST':
		if request.POST['button'] == 'Cancel':
			cancel_pickup = request.POST.get('cancel')
			Order.objects.filter(pk=cancel_pickup).update(pickupstat_id='Cancelled')
		elif request.POST['button'] == 'Receive Payment':
			transac_successful = request.POST.get('transaction-successful')
			Order.objects.filter(pk=transac_successful).update(pickupstat_id='Transaction Successful')
			return HttpResponseRedirect(reverse('sales-invoice', args=[str(transac_successful)]))

	#SEARCH
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	orders = OrderPickUp.objects.filter(order__complete=True, order__customer=customer).order_by('-order__date_ordered')
	filter = OrderPickUp.objects.filter(
		Q(order__transaction_id__icontains=q) |
		Q(order__pickupstat_id__icontains=q) 
	)

	#PAGE NAVIGATION
	paginator = Paginator(filter, 5)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context = {'items':items, 'orders':orders, 'page_prod': page_prod, 'current_datetime':current_datetime, 'filter': filter}
	return render(request, 'base/otc-products/client/my-purchases.html', context)

#REVIEW
def review(request, pk):
	order = Order.objects.get(id=pk)
	form = ReviewForm(instance=order)

	customer = request.user.customer
	items = OrderItem.objects.filter(order=order, order__customer=customer).order_by('-id')
	review = CustomerReview.objects.filter(orderpickup__order=order).order_by('-last_updated')

	
	item = OrderItem.objects.filter(order=order, order__customer=customer)
	product = otcProduct.objects.get(orderitem__in=item)
	orderpickup = OrderPickUp.objects.get(order=order,order__customer=customer, order__complete=True)
	
	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
					
			review = CustomerReview.objects.create(
			customer = customer,	
			product = product,
			orderpickup = orderpickup,
			review = instance.review,
			is_like = instance.is_like,
			is_dislike = instance.is_dislike,
			last_updated = instance.last_updated
			)
			review.save()

			return redirect('my-purchases')

	context = {'form': form, 'items': items, 'review': review, 'product': product}
	return render(request, 'base/otc-products/client/review.html', context)

#UPDATE ITEM RENDER VIEW
@login_required(login_url="/login")
# @user_passes_test(admin_test, login_url="/shop/otc/products/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
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
@user_passes_test(admin_test, login_url="/shop/pending-reservations/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
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
@user_passes_test(admin_test, login_url="/shop/pending-reservations/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
def order_items(request, pk):
	order = Order.objects.get(id=pk)
	orderitems = OrderItem.objects.filter(order=order).order_by('-id')

	context = {'order': order, 'orderitems': orderitems}
	return render(request, 'base/otc-products/admin/order-details.html', context)

#ADMIN VIEW: APPROVAL OF ORDERS
@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/shop/approved-reservations/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
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

	#PAGE NAVIGATION
	paginator = Paginator(reservations, 5)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context = {'orders': orders, 'items': items, 'page_prod': page_prod, 'current_datetime':current_datetime,  }
	return render(request, 'base/otc-products/admin/approved-reservations.html', context)

#ADMIN VIEW: COMPLETED ORDERS
@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/shop/completed-reservations/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
def completed_orders(request):
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
	return render(request, 'base/otc-products/admin/completed-reservations.html', context)

def all_orders(request):
	current_datetime = datetime.now()
	items = OrderItem.objects.all()
	
	#COUNT
	transaction_count = Order.objects.filter(pickupstat_id='Transaction Successful').count()
	approve_count = Order.objects.filter(pickupstat_id='Approved').count()
	pending_count = Order.objects.filter(pickupstat_id='Pending').count()
	cancelled_count = Order.objects.filter(pickupstat_id='Cancelled').count()
	complete_count = Order.objects.filter(pickupstat_id='Transaction Successful').count()

	#SEARCH
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	reservations = OrderPickUp.objects.filter(order__complete=True).order_by('-date_added')
	orders = OrderPickUp.objects.filter(
		Q(order__transaction_id__icontains=q) |
		Q(pickup__icontains=q) 
	)

	#PAGE NAVIGATION
	paginator = Paginator(reservations, 5)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context = {'orders': orders, 'items': items, 'page_prod': page_prod, 'current_datetime':current_datetime, 'transaction_count': transaction_count, 'approve_count': approve_count, 'pending_count': pending_count, 'cancelled_count': cancelled_count, 'complete_count': complete_count }
	return render(request, 'base/otc-products/admin/all-reservations.html', context)


#ADMIN VIEW: SALES INVOICE RENDER VIEW
@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/shop/completed-reservations/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
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
	
			itemquanti = OrderItem.objects.filter(order=invoice.order.id)

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

#----------------------------------------------------ADMIN VIEW: PRODUCT RESERVATION SALES
@login_required(login_url="/login")
@user_passes_test(admin_test, login_url="/shop/product-sales-reports/go_back")
# @user_passes_test(admin_test, login_url="/shop/otc/create-product/go_back")
def prod_reservation_sales(request):

	current_datetime = datetime.now()
	items = OrderItem.objects.all()
	reservations = OrderPickUp.objects.all()

	#DATE FROM TO RANGE FILTER
	if request.method == 'POST':
		if request.POST['button'] == "Search":
			fromdate=request.POST.get('fromdate')
			request.session['fromdate'] = fromdate
			todate = request.POST.get('todate')
			request.session['todate'] = todate
			reservations = OrderPickUp.objects.filter(pickup__gte=fromdate,pickup__lte=todate).order_by('-pickup')

	#COUNT
	orders = Order.objects.filter(pickupstat_id='Transaction Successful').first()
	sales_count = Order.objects.filter(pickupstat_id='Transaction Successful').count()
	approve_count = Order.objects.filter(pickupstat_id='Approved').count()
	pending_count = Order.objects.filter(pickupstat_id='Pending').count()
	cancelled_count = Order.objects.filter(pickupstat_id='Cancelled').count()
	complete_count = Order.objects.filter(pickupstat_id='Transaction Successful').count()

	total_sales = OrderPickUp.objects.filter(order__pickupstat_id='Transaction Successful').values('order').aggregate(
        total=Sum(
            F("order__orderitem__quantity") * F("order__orderitem__product__Prod_Price"),
            output_field=FloatField()
        )
    )
	reservations = OrderPickUp.objects.filter(order__complete=True, order__pickupstat_id='Transaction Successful').order_by('-pickup')

	#PAGE NAVIGATION
	paginator = Paginator(reservations, 5)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	context = {'total_sales': total_sales, 'orders': orders, 'items': items, 'reservations': reservations, 'page_prod': page_prod, 'current_datetime':current_datetime, 'sales_count': sales_count, 'approve_count': approve_count, 'pending_count': pending_count, 'complete_count': complete_count, 'cancelled_count': cancelled_count}
	return render(request, 'base/otc-products/admin/product-sales-reports.html', context)

# PRODUCT RESERVATION SALES REPORT ---------------------------------------------
def pdf_report_create_product_sales(request):	
	items = OrderItem.objects.all()
	current_datetime = datetime.now()
	reservations = OrderPickUp.objects.all()
	
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


	#COUNT
	sales_count = Order.objects.filter(pickupstat_id='Transaction Successful').count()
	stat_id = ['Pending', 'Approved','Cancelled', 'Transaction Successful', 'Confirmed']
	
	# FOR GETTING DISTINCT CUSTOMERS
	oi = OrderItem.objects.all().distinct()
	oi1 = []
	for row in oi:
		oi1.append(row.order_id)
	cust_count = Order.objects.filter(pk__in=oi1).values('customer').distinct().count()

	# SELECT COUNT(DISTINCT customer_id) AS TotalCust FROM base_orderitem INNER JOIN base_order ON base_orderitem.order_id = base_order.id;
	
	# FOR GETTING TOTAL PRODUCTS SOLD
	products_sold = 0
	for row in items:
		products_sold = products_sold + int(row.quantity)

	# FOR GETTING TOTAL EARNINGS
	total_sales = OrderPickUp.objects.filter(order__pickupstat_id='Transaction Successful').values('order').aggregate(
        total=Sum(
            F("order__orderitem__quantity") * F("order__orderitem__product__Prod_Price"),
            output_field=FloatField()
        )
    )

	#SEARCH -- MIGHT CHANGE LATER
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	reservations = OrderPickUp.objects.filter(order__complete=True, order__pickupstat_id='Transaction Successful').order_by('-pickup')
	orders = OrderPickUp.objects.filter(
		Q(order__transaction_id__icontains=q) |
		Q(pickup__icontains=q) 
	)

	paginator = Paginator(orders, 500)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	template_path = 'base/otc-products/admin/product-sales-reports-pdf.html' 
	context = {'orders': orders, 'items': items, 'reservations': reservations,'page_prod': page_prod, 'sales_count': sales_count, 'current_datetime':current_datetime, 'products_sold':products_sold, 'stat_id':stat_id, 'cust_count':cust_count, 'total_sales':total_sales}
    # Create a Django response object, and specify content_type as pdf 
	response = HttpResponse(content_type='application/pdf') 
	response['Content-Disposition'] =  'filename="product-sales-report.pdf"'
    # find the template and render it.

	template = get_template(template_path)  
	html = template.render(context)

    # create a pdf  
	pisa_status = pisa.CreatePDF(
       html, dest=response)

	if pisa_status.err:
     
	   return HttpResponse('We had some errors <pre>' + html + '</pre>')
	
	return response

def all_orders_report(request):
	items = OrderItem.objects.all()
	current_datetime = datetime.now()
	
	# FOR GETTING DISTINCT CUSTOMERS
	oi = OrderItem.objects.all().distinct()
	oi1 = []
	for row in oi:
		oi1.append(row.order_id)
	cust_count = Order.objects.filter(pk__in=oi1).values('customer').distinct().count()

	#COUNT
	transaction_count = Order.objects.filter(pickupstat_id='Transaction Successful').count()
	approve_count = Order.objects.filter(pickupstat_id='Approved').count()
	pending_count = Order.objects.filter(pickupstat_id='Pending').count()
	cancelled_count = Order.objects.filter(pickupstat_id='Cancelled').count()
	complete_count = Order.objects.filter(pickupstat_id='Transaction Successful').count()
	reservation_count = approve_count + pending_count + cancelled_count + complete_count

	#SEARCH
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	reservations = OrderPickUp.objects.filter(order__complete=True).order_by('-date_added')
	orders = OrderPickUp.objects.filter(
		Q(order__transaction_id__icontains=q) |
		Q(pickup__icontains=q) 
	)

	#PAGE NAVIGATION
	paginator = Paginator(reservations, 500)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	template_path = 'base/otc-products/admin/all-reservations-pdf.html' 
	context = {'orders': orders, 'items': items, 'page_prod': page_prod, 'cust_count':cust_count, 'transaction_count': transaction_count, 'approve_count': approve_count, 'pending_count': pending_count, 'cancelled_count': cancelled_count, 'complete_count': complete_count, 'reservation_count':reservation_count, 'current_datetime':current_datetime }
    # Create a Django response object, and specify content_type as pdf 
	response = HttpResponse(content_type='application/pdf') 
	response['Content-Disposition'] =  'filename="all-orders-report.pdf"'
    # find the template and render it.

	template = get_template(template_path)  
	html = template.render(context)

    # create a pdf  
	pisa_status = pisa.CreatePDF(
       html, dest=response)

	if pisa_status.err:
       
	   return HttpResponse('We had some errors <pre>' + html + '</pre>')
	
	return response

def otcProductlogreport(request):
	history = otcStockHistory.objects.all().order_by('-last_updated')

	#PAGE NAVIGATION
	paginator = Paginator(history, 1000)
	page_number = request.GET.get('page')
	page_prod = paginator.get_page(page_number)

	
	template_path = 'base/otc-products/admin/products-history-pdf.html' 
	context = {'history': history, 'page_prod': page_prod}
    # Create a Django response object, and specify content_type as pdf 
	response = HttpResponse(content_type='application/pdf') 
	response['Content-Disposition'] =  'filename="product-log-report.pdf"'
    # find the template and render it.

	template = get_template(template_path)  
	html = template.render(context)

    # create a pdf  
	pisa_status = pisa.CreatePDF(
       html, dest=response)

	if pisa_status.err:
       
	   return HttpResponse('We had some errors <pre>' + html + '</pre>')
	
	return response

def otc_indivProductHistoryreport(request, pk):
	product = otcProduct.objects.get(id=pk)
	history = otcStockHistory.objects.filter(Prod_Name=product).order_by('-last_updated')

	template_path =  'base/otc-products/admin/indiv-products-history-pdf.html' 
	context = {'product': product, 'history': history}
    # Create a Django response object, and specify content_type as pdf 
	response = HttpResponse(content_type='application/pdf') 
	response['Content-Disposition'] =  'filename="indiv-product-log-report.pdf"'
    # find the template and render it.

	template = get_template(template_path)  
	html = template.render(context)

    # create a pdf  
	pisa_status = pisa.CreatePDF(
       html, dest=response)

	if pisa_status.err:
       
	   return HttpResponse('We had some errors <pre>' + html + '</pre>')
	
	return response

def salesinvoicereport(request, pk):
	items = OrderItem.objects.all()
	invoice = OrderPickUp.objects.get(order__id=pk)
	
	if request.method =='POST':
		if request.POST['button'] == 'Confirm':
	     
			itemquanti = OrderItem.objects.filter(order=invoice.order.id)

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


	template_path = 'base/otc-products/admin/sales-invoice-pdf.html'
	context = {'invoice': invoice, 'items': items}
    # Create a Django response object, and specify content_type as pdf 
	response = HttpResponse(content_type='application/pdf') 
	response['Content-Disposition'] =  'filename="salew-invoice.pdf"'
    # find the template and render it.

	template = get_template(template_path)  
	html = template.render(context)

    # create a pdf  
	pisa_status = pisa.CreatePDF(
       html, dest=response)

	if pisa_status.err:
       
	   return HttpResponse('We had some errors <pre>' + html + '</pre>')
	
	return response

