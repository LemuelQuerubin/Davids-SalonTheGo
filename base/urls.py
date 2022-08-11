from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('ins/products/<str:pk>/', views.ins_indivProduct, name="ins-individual-product"),
    path('ins/create-product/', views.ins_createProduct, name="ins-create-product"),
    path('ins/update-product/<str:pk>/', views.ins_updateProduct, name="ins-update-product"),

    #OTC PRODUCTS (ADMIN SIDE)
    path('otc/products/', views.otcProducts, name="otc-products"),
    path('otc/products/<str:pk>/', views.otc_indivProduct, name="otc-individual-product"),
    path('otc/products/history/<str:pk>/', views.otc_indivProductHistory, name="otc-individual-product-history"),
    path('deduct-stock/<str:pk>/', views.deduct_items, name="deduct-stock"),
    path('restock/<str:pk>/', views.add_items, name="restock"),
    path('otc/history/', views.otc_history, name='otc-history'),

    path('otc/create-product/', views.otc_createProduct, name="otc-create-product"),
    path('otc/update-product/<str:pk>/', views.otc_updateProduct, name="otc-update-product"),
        #DELETE / path('delete-product/<str:pk>/', views.deleteProduct, name="delete-product"),

    #CART
    path('cart/', views.cart, name="cart"),
	#path('shop/cart/', views.cart, name="cart"),
    
    #CHECKOUT
	path('checkout/', views.checkout, name="checkout"),
    #path('shop/checkout/', views.checkout, name="checkout"),

    #MY PURCHASES
	path('my-purchases/', views.my_purchases, name="my-purchases"),
    path('review/<str:pk>', views.review, name="review"),

    #SALES INVOICE
	path('sales-invoice/<str:pk>/', views.salesinvoice, name="sales-invoice"),

    #ADMIN: VIEW RESERVATIONS | APPROVE/REJECT
    path('pending-reservations/', views.pending_orders, name="pending-reservations"),
    path('approved-reservations/', views.approved_orders, name="approved-reservations"),
    path('completed-reservations/', views.completed_orders, name="completed-reservations"),
    path('all-reservations/', views.all_orders, name="all-reservations"),
    
    # ----- VIEW ORDER DETAILS
    path('order-items/<str:pk>/', views.order_items, name="order-details"),
    # REPORT GENERATIONS
    # PRODUCT RESERVATION SALES
    path('product-sales-reports/', views.prod_reservation_sales, name="product-sales-reports"),

    path('createpdf-productsales/', views.pdf_report_create_product_sales, name='createpdfproduct'),

    path('createpdf-all-reservations/', views.all_orders_report, name='createpdf-all-reservations'),

    path('createpdf-product-log/', views.otcProductlogreport, name='createpdf-product-log'),

    path('createpdf-indiv-product-log/<str:pk>/', views.otc_indivProductHistoryreport, name='createpdf-indiv-product-log'),
    
    path('createpdf-sales-invoice/<int:pk>/', views.salesinvoicereport, name="createpdf-sales-invoice"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

