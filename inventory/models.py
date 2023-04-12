from django.db import models
from account.models import User
# Create your models here.

class Ingredient(models.Model):
	#add name of ingredient
	#add price per unit
	#how much item available
	UNIT_CHOICES=[
	('l','litres'),
	('ml','millilitres'),
	('g','grams'),
	('kg','kilograms'),
	('oz','ounce'),
	('co','count')]
	title=models.CharField(max_length=50)
	unit=models.CharField(max_length=2,choices=UNIT_CHOICES)
	quantity=models.FloatField()
	price=models.FloatField()
	def __str__(self):
		return self.title


class MenuItem(models.Model):
	title=models.CharField(max_length=50)
	ingredient=models.ManyToManyField(Ingredient,through='RecipeRequirement')
	price=models.FloatField(help_text='$')
	
	def all_ingredient(self):
		return ','.join([item.title for item in self.ingredient.all()])
	def menu_cost(self):
		cost=0
		for item in self.ingredient.all():
			cost+=item.price
		return cost


	def __str__(self):
		return self.title+f' ({self.price}$)'

		

class RecipeRequirement(models.Model):
	ingredient=models.ForeignKey(Ingredient,on_delete=models.CASCADE)
	menu=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
	quantity=models.FloatField()
		
class Customer(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	menu=models.ManyToManyField(MenuItem,through='Purchase')
	order_time=models.DateTimeField(auto_now_add=True)

	def menu_list(self):
		return ','.join([menu.title for menu in self.menu.all()])
	# def __str__(self):
	# 	return self.user.username

class Purchase(models.Model):
	#add customer purchase
	#inventory should be modified
	#record time that purches was made
	order=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
	customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
	


