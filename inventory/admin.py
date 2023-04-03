from django.contrib import admin
from .models import Ingredient, MenuItem,Purchase

class IngredientInline(admin.TabularInline):
    model = MenuItem.ingredient.through
    extra = 1

class MenuItemAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    exclude=('ingredient',)

admin.site.register(MenuItem,MenuItemAdmin)
admin.site.register(Ingredient)

class PurchaseAdmin(admin.ModelAdmin):
    list_display=['pk','orders','order_time']
admin.site.register(Purchase,PurchaseAdmin)