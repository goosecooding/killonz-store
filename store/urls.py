from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('product/<slug:slug>/', views.product_detail, name='product'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('repair/', views.repair_request, name='repair'),

    # Owner dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/orders/', views.dashboard_orders, name='dashboard_orders'),
    path('dashboard/orders/<int:order_id>/', views.dashboard_order_detail, name='dashboard_order_detail'),
    path('dashboard/orders/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    path('dashboard/repairs/', views.dashboard_repairs, name='dashboard_repairs'),
    path('dashboard/repairs/<int:repair_id>/status/', views.update_repair_status, name='update_repair_status'),
    path('dashboard/products/', views.dashboard_products, name='dashboard_products'),
    path('dashboard/products/add/', views.product_add, name='product_add'),
    path('dashboard/products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('dashboard/products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('dashboard/products/<int:product_id>/toggle-stock/', views.toggle_stock, name='toggle_stock'),
    path('dashboard/categories/', views.dashboard_categories, name='dashboard_categories'),
    path('dashboard/categories/add/', views.category_add, name='category_add'),
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),
]
