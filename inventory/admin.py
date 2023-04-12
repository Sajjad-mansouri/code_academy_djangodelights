from django.contrib import admin
from .models import Ingredient, MenuItem,Purchase,Customer

class IngredientInline(admin.TabularInline):
    model = MenuItem.ingredient.through
    extra = 1

class MenuItemAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    exclude=('ingredient',)
    list_display=('title','all_ingredient','menu_cost')

admin.site.register(MenuItem,MenuItemAdmin)
admin.site.register(Ingredient)



class PurchaseInline(admin.TabularInline):
    model = Customer.menu.through
    extra = 1
class PurchaseAdmin(admin.ModelAdmin):
    inlines = [PurchaseInline]
    list_display=['user','menu_list']

# class PurchaseAdmin(admin.ModelAdmin):
#     list_display=['pk','order','order_time']
admin.site.register(Customer,PurchaseAdmin)