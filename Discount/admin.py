from django.contrib import admin
from .models import Discount
from django.utils.html import format_html

class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'amount', 'expiration_date', 'is_active', 'description', 
        'applicable_to', 'product', 'category', 'user_group', 'min_quantity', 'status_display'
    )
    list_filter = ('is_active', 'product', 'category', 'user_group')
    search_fields = ('code', 'description')
    ordering = ('-expiration_date',)
    list_per_page = 20
    
    def status_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">Active</span>')
        else:
            return format_html('<span style="color: red;">Inactive</span>')
    status_display.short_description = 'Status'

    fieldsets = (
        (None, {
            'fields': ('code', 'amount', 'expiration_date', 'is_active', 'description', 'applicable_to', 'product', 'category', 'user_group', 'min_quantity')
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

admin.site.register(Discount, DiscountAdmin)
