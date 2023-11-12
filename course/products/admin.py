from django.contrib import admin
from django.db.models import Q
from import_export import resources
from import_export.admin import ExportMixin
from import_export.formats import base_formats
from simple_history.admin import SimpleHistoryAdmin
from import_export.fields import Field
from import_export.widgets import DecimalWidget
from decimal import Decimal

from .models import Product, Cart, CartItem, Category


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'categories', 'stock_quantity', 'date_created')
        export_order = ('id', 'name', 'description', 'price', 'categories', 'stock_quantity', 'date_created')



    def dehydrate_price(self, product):
        formatted_price = f"${product.price:.2f}"
        return formatted_price

    def get_description(self, product):
        return product.description.upper()



class CartResource(resources.ModelResource):
    class Meta:
        model = Cart


class CartItemResource(resources.ModelResource):
    class Meta:
        model = CartItem


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class CustomModelAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    pass


class ProductInline(admin.TabularInline):
    model = Product.categories.through


class CategoryAdmin(ExportMixin,CustomModelAdmin):
    resource_class = CategoryResource
    inlines = [ProductInline]
    list_display = ['name', 'get_attached_products']
    filter_horizontal = ('products',)

    def get_attached_products(self, obj):
        products = obj.products.all()
        return ", ".join([product.name for product in products])


class ProductAdmin(ExportMixin,CustomModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'description', 'price', 'date_created')
    readonly_fields = ('date_created',)
    filter_horizontal = ('categories',)
    list_filter = ('categories', 'date_created',)
    date_hierarchy = 'date_created'
    list_display_links = ('name', 'price', 'description',)
    search_fields = ['name', 'description']

    def get_export_queryset(self, request):
        return Product.objects.filter(price__gt=100)

    def get_export_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]




class CartAdmin(ExportMixin,CustomModelAdmin):
    resource_class = CartResource
    list_display = ('user', 'total_price')

    class CartItemInline(admin.TabularInline):
        model = CartItem
        extra = 0

    inlines = [CartItemInline]


class CartItemAdmin(ExportMixin,CustomModelAdmin):
    resource_class = CartItemResource
    list_display = ('cart', 'product', 'quantity', 'subtotal')
# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
