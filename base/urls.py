from django.urls import path
from . import views

urlpatterns = [

    #JSON Response
	path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    #path('', views.home, name="home"),

    path('', views.shop, name="shop"),
    #path('shop/<str:pk>/', views.shopIndivProduct, name="shop-individual-product"),
    path('<int:pk>/', views.shopIndivProduct, name="shop-individual-product"),
    
    #INSALON PRODUCTS (ADMIN SIDE)
    path('ins/products/', views.insProducts, name="ins-products"),
    #VIEW INSALON PRODUCTS (ADMIN SIDE)
    path('ins/products/<str:pk>/', views.ins_indivProduct, name="ins-individual-product"),
    
    #CREATE AND UPDATE NEW INS PRODUCT
    path('ins/create-product/', views.ins_createProduct, name="ins-create-product"),
    path('ins/update-product/<str:pk>/', views.ins_updateProduct, name="ins-update-product"),

    #OTC PRODUCTS (ADMIN SIDE)
    path('otc/products/', views.otcProducts, name="otc-products"),
    path('otc/products/<str:pk>/', views.otc_indivProduct, name="otc-individual-product"),

    path('otc/create-product/', views.otc_createProduct, name="otc-create-product"),
    path('otc/update-product/<str:pk>/', views.otc_updateProduct, name="otc-update-product"),
        #DELETE / path('delete-product/<str:pk>/', views.deleteProduct, name="delete-product"),

    #CART
    path('cart/', views.cart, name="cart"),
	#path('shop/cart/', views.cart, name="cart"),
    
    #CHECKOUT
	path('checkout/', views.checkout, name="checkout"),
    #path('shop/checkout/', views.checkout, name="checkout"),

    #--------------------------MY PURCHASES--------------------------
    #NEEDS FIXING - LOOP
	path('mypurchases/', views.mypurchases, name="mypurchases"),

    #--------------------------SALES INVOICE--------------------------
	path('sales-invoice/<str:pk>/', views.salesinvoice, name="sales-invoice"),

    #ADMIN: VIEW RESERVATIONS | APPROVE/REJECT
    path('pending-reservations/', views.pending_orders, name="pending-reservations"),
    path('approved-reservations/', views.approved_orders, name="approved-reservations"),
    # ----- VIEW ORDER DETAILS
    path('order-items/<str:pk>/', views.order_items, name="order-details"),
]