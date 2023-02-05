from django.contrib import admin 
from models import *
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = UserRegistrationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Registration Form',
            {
                'fields': (
                    'username',
                )
            }
        )
    )

class PriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInlineAdmin]

admin.site.register(File, ProductAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(CustomLogin)
