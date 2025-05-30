import xlrd
from products import models
from mainapp.models import Ingredient, CategoryIngredient

def parse_products():
    workbook = xlrd.open_workbook("products.xlsx")

    worksheet = workbook.sheet_by_index(0)

    for i in range(1, 95):
        category = models.Category.objects.get(id=int(worksheet.cell_value(i, 3)))
        new_product = models.Product.objects.create(title=worksheet.cell_value(i, 0), category=category, price=worksheet.cell_value(i, 1),
                                                    weight=worksheet.cell_value(i, 2), description=worksheet.cell_value(i, 4), composition=worksheet.cell_value(i, 5),
                                                    image=f"image_large/{worksheet.cell_value(i, 6)}")
        new_product.save()

def parse_ingredients():

    workbook = xlrd.open_workbook("Ingridients.xlsx")

    worksheet = workbook.sheet_by_index(0)

    for i in range(1, 33):
        category = CategoryIngredient.objects.get(title=worksheet.cell_value(i, 2))
        new_ing = Ingredient.objects.create(title=worksheet.cell_value(i, 0), category=category,
                                                    price=worksheet.cell_value(i, 1))
        if worksheet.cell_value(i, 3):
            new_ing.cover = f"image_ing/{worksheet.cell_value(i, 3)}"
        new_ing.save()