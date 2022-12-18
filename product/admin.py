from django.contrib import admin
from .models import Product, Category, Manufacturer, Color, Type, Comment

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

class ManufacturerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

class ColorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('color',)}

class TypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('type',)}

admin.site.register(Product)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Comment)