from django.contrib import admin
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug', 'order']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'category', 'price', 'is_in_stock', 'is_featured']
    list_filter = ['category', 'is_in_stock', 'is_featured']
    list_editable = ['is_in_stock', 'is_featured', 'price']
    search_fields = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'phone', 'email', 'wilaya', 'status', 'total', 'created_at']
    list_filter = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at']
