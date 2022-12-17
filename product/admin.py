from django.contrib import admin
from .models import Product, Category, Manufacturer

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

class ManufacturerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}


admin.site.register(Product)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)