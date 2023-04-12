from django.urls import path
from .views import ( HomePageView,
				MenuView,
				InventoryView,
				CustomerView,
				MenuIngredientView,
				CreateMenu,
				UpdateMenu,
				DeleteMenu,
				PurchaseList,
				Purchase,
				CreateIngredient,
				UpdateIngredient,
				DeleteIngredient,
				IngredientView,
				purchase,
				Profit
				 )

urlpatterns=[
path('',HomePageView.as_view(),name='home'),
path('inventory/',InventoryView.as_view(),name='inventory'),
path('inventory/menu/',MenuView.as_view(),name='menu'),
path('customer/',CustomerView.as_view(),name='customer'),
path('inventory/menu/<pk>',MenuIngredientView.as_view(),name='menu-ingredient'),
path('inventory/menu/create/',CreateMenu.as_view(),name='create-menu'),
path('inventory/menu/update/<pk>/',UpdateMenu.as_view(),name='update-menu'),

path('inventory/menu/delete/<pk>/',DeleteMenu.as_view(),name='delete-menu'),
path('inventory/ingredient/create/',CreateIngredient.as_view(),name='create-ingredient'),
path('inventory/ingredient/update/<pk>/',UpdateIngredient.as_view(),name='update-ingredient'),
path('inventory/ingredient/delete/<pk>/',DeleteIngredient.as_view(),name='delete-ingredient'),
path('inventory/ingredient/',IngredientView.as_view(),name='ingredient'),
path('customer/<int:pk>/',PurchaseList.as_view(),name='purchase-list'),
path('customer/purchase',purchase,name='purchase'),
path('customer/profit',Profit.as_view(),name='profit'),

]