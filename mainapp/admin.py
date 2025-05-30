from django.contrib import admin
from . import models

admin.site.register(models.Receipt)
admin.site.register(models.CategoryIngredient)
admin.site.register(models.Ingredient)
admin.site.register(models.Cake)
admin.site.register(models.Floor)