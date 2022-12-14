from django.contrib import admin

from store.models import Product, Variation


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'stock', 'is_available',
                    'category', 'price', 'created_date', ]
    prepopulated_fields = {'slug': ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ["product", "variation_category",
                    "variation_value", "is_active"]
    list_filter = ["product", "variation_value", "variation_value"]
    list_editable = ["is_active", "variation_value"]


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
