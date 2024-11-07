from django.contrib import admin

from web.models import Product, Category, Coupon

admin.site.register(Category)
admin.site.register(Coupon)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    list_editable = ('price',)
    ordering = ('name', 'price')



