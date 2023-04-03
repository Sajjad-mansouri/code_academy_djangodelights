from django.db import models

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
	quantity=models.FloatField(help_text='(Kg)')
	price=models.FloatField(help_text='$')
	def __str__(self):
		return self.title


class MenuItem(models.Model):
	title=models.CharField(max_length=50)
	ingredient=models.ManyToManyField(Ingredient,through='RecipeRequirement')
	price=models.FloatField(help_text='$')
	
	def __str__(self):
		return self.title

		

class RecipeRequirement(models.Model):
	ingredient=models.ForeignKey(Ingredient,on_delete=models.CASCADE)
	menu=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
	quantity=models.FloatField()
		

class Purchase(models.Model):
	#add customer purchase
	#inventory should be modified
	#record time that purches was made
	order=models.ManyToManyField(MenuItem)
	order_time=models.DateTimeField(auto_now_add=True)

	def orders(self):
		return ','.join([item.title for item in self.order.all()])
