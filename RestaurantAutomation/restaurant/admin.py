from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', 
        {
            'fields': ('is_customer', 'name', 'phone_number', 'validated'),
        }),
    )
    list_display = ('name', 'email', 'validated')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)

# customize admin interface
admin.site.site_header = "Restaurant Automation Administration"
admin.site.site_title = "Restaurant Automation Admin Portal"
admin.site.index_title = "Welcome to Restaurant Automation Admin Portal"
