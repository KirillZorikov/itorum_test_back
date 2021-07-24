from django.contrib import admin

from .models import Customer, ExportAccess, Order

for model in (Customer, ExportAccess):
    admin.site.register(model)

@admin.register(Order)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('customer', 'price', 'created_at')
    list_filter = ('customer',)
