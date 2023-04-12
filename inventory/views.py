from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView ,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count,Sum,F
from django.http import HttpResponse
from .models import Ingredient,MenuItem,Customer,Purchase,RecipeRequirement
from .forms import MenuForm,IngredientFormSet ,CustomerForm,PurchaseFormSet
from account.models import User

class HomePageView(TemplateView):
	template_name='inventory/home.html'

class CustomerView(LoginRequiredMixin,TemplateView):
	template_name='inventory/customer.html'

class InventoryView(LoginRequiredMixin,TemplateView):
	template_name='inventory/inventory.html'



class MenuView(LoginRequiredMixin,ListView):
	model=MenuItem
	template_name='inventory/Menu.html'

class CreateMenu(LoginRequiredMixin,CreateView):
	form_class=MenuForm 
	template_name='inventory/create_menu.html'
	success_url=reverse_lazy('menu')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = IngredientFormSet(self.request.POST)
		else:
			context['formset'] = IngredientFormSet()
		return context



	def form_valid(self,form):
		context=self.get_context_data()
		formset=context['formset']
		if formset.is_valid() and form.is_valid():
			self.object=form.save()
			formset.instance=self.object
			formset.save()
			return super().form_valid(form)

class UpdateMenu(LoginRequiredMixin,UpdateView):
	model=MenuItem
	form_class=MenuForm 
	template_name='inventory/create_menu.html'
	success_url=reverse_lazy('menu')

	def get_context_data(self, **kwargs):
		
		context = super().get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = IngredientFormSet(self.request.POST,instance=self.object)
		else:
			context['formset'] = IngredientFormSet(instance=self.object)
		return context
	def form_valid(self,form):
		context=self.get_context_data()
		formset=context['formset']

		if formset.is_valid() and form.is_valid():
			form.save()
			formset.save()
			return super().form_valid(form)
		else:
			return self.form_invalid(form)
	def form_invalid(self, form):
		context = self.get_context_data()
		formset = context['formset']

		# Add form and formset errors to the response
		response = super().form_invalid(form)
		response.context_data['form_errors'] = form.errors
		response.context_data['formset_errors'] = formset.errors

		return response
class DeleteMenu(DeleteView):
	model=MenuItem
	template_name='inventory/delete_confirm_view.html'
	context_object_name='object'
	success_url=reverse_lazy('menu')
		
class MenuIngredientView(LoginRequiredMixin,DetailView):
	model=MenuItem
	template_name='inventory/menu-ingredient.html'

	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		pk=self.kwargs.get('pk')
		menu=MenuItem.objects.get(pk=pk)
		ingredients=menu.ingredient.all()
		reciperequirements=menu.reciperequirement_set.all()
		context['ingredients']=ingredients
		context['reciperequirements']=reciperequirements
		return context


class IngredientView(LoginRequiredMixin,ListView):
	model=Ingredient
	template_name='inventory/ingredient.html'
	context_object_name='ingredients'


class CreateIngredient(LoginRequiredMixin,CreateView):
	model=Ingredient
	template_name='inventory/create-ingredient.html'
	fields=['title','unit','quantity','price']
	success_url=reverse_lazy('ingredient')
class UpdateIngredient(LoginRequiredMixin,UpdateView):
	model=Ingredient
	template_name='inventory/create-ingredient.html'
	fields=['title','unit','quantity','price']
	success_url=reverse_lazy('ingredient')
class DeleteIngredient(DeleteView):
	model=Ingredient
	context_object_name='object'
	template_name='inventory/delete_confirm_view.html'
	success_url=reverse_lazy('ingredient')

class PurchaseList(LoginRequiredMixin,ListView):
	model=Customer
	template_name='inventory/purchase-list.html'
	context_object_name='orders'

	def get_queryset(self):
		pk=self.kwargs.get('pk')
		user=User.objects.get(pk=pk)
		return Customer.objects.filter(user=user)





def purchase(request):
	menu_requierment={}
	total_ingredient={}
	for item in RecipeRequirement.objects.all():
			menu_requierment[item.ingredient.title]=item.quantity
	for ingredient in Ingredient.objects.all():
			total_ingredient[ingredient.title]=ingredient.quantity
	for x,y in menu_requierment.items():
					if  menu_requierment[x] > total_ingredient[x]:
						MenuItem.objects.filter(ingredient=Ingredient.objects.get(title=x)).delete()
						break

	form=PurchaseFormSet()
	if request.method=='POST':
		form=PurchaseFormSet(request.POST)
		if form.is_valid():
			
			#form(instance=user,initial=[{'user':request.user}])
			form.save(commit=False)
			
			
			
			total_ingredient={}
			menu_requierment={}
			for field in form.cleaned_data:
				
				# for item in RecipeRequirement.objects.filter(menu=field['order'].pk):
				# 	print(item.ingredient,item.quantity)
				if not field :
					return render(request,'inventory/purchase.html',{'form':form})
				

				for item in field['order'].reciperequirement_set.all():
					menu_requierment[item.ingredient.title]=item.quantity

				for ingredient in field['order'].ingredient.all():
					total_ingredient[ingredient.title]=ingredient.quantity
					
				
				for x,y in menu_requierment.items():
					total_ingredient[x]=total_ingredient[x]-y
					Ingredient.objects.filter(title=x).update(quantity=total_ingredient[x])
				
			user=Customer.objects.create(user=request.user)
			form.instance=user
			form.save()
			


			
			return redirect('purchase-list',pk=request.user.id)
			

	return render(request,'inventory/purchase.html',{'form':form})



class Profit(LoginRequiredMixin,TemplateView):
	template_name='inventory/profit.html'
	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		income=Purchase.objects.aggregate(income=Sum('order__price'))
		cost=Purchase.objects.aggregate(cost=Sum(F('order__reciperequirement__ingredient__price')*F('order__reciperequirement__quantity')))
		context['income']=income['income']
		context['cost']=cost['cost']
		context['profit']=income['income']-cost['cost']
		return context

