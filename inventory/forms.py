from django import forms
from .models import MenuItem ,Ingredient,Customer,Purchase



class MenuForm(forms.ModelForm):
	
	
	class Meta:
		model=MenuItem
		fields=('title','price')

	class Media:
		css = {'all': ('admin/css/forms.css', 'admin/css/base.css', 'admin/css/changelists.css', 'admin/css/widgets.css')}
		#js = ('admin/js/core.js', 'admin/js/vendor/jquery/jquery.js', 'admin/js/jquery.init.js','admin/js/admin/RelatedObjectLookups.js','admin/js/inlines.js','admin/js/core.js')
		js=('inventory/js/jquery-3.6.4.min.js','inventory/js/my_js.js')


IngredientFormSet = forms.inlineformset_factory(
		MenuItem,
		MenuItem.ingredient.through,
		form=MenuForm,
		fields=['ingredient','quantity'],
		extra=1,
		can_delete=True
	)

class CustomerForm(forms.ModelForm):
	class Meta:
		model=Customer
		fields=('user',)
	class Media:
		css = {'all': ('admin/css/forms.css', 'admin/css/base.css', 'admin/css/changelists.css', 'admin/css/widgets.css')}
		#js = ('admin/js/core.js', 'admin/js/vendor/jquery/jquery.js', 'admin/js/jquery.init.js','admin/js/admin/RelatedObjectLookups.js','admin/js/inlines.js','admin/js/core.js')
		js=('inventory/js/jquery-3.6.4.min.js','inventory/js/my_js.js')

PurchaseFormSet = forms.inlineformset_factory(
		Customer,
		Purchase,
		form=CustomerForm,
		fields=['order',],
		extra=1,
		can_delete=True
	)