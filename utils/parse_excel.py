import xlrd
from products import models


def parse():
    workbook = xlrd.open_workbook("products.xlsx")

    worksheet = workbook.sheet_by_index(0)

    for i in range(1, 95):
        category = models.Category.objects.get(id=int(worksheet.cell_value(i, 3)))
        new_product = models.Product.objects.create(title=worksheet.cell_value(i, 0), category=category, price=worksheet.cell_value(i, 1),
                                                    weight=worksheet.cell_value(i, 2), description=worksheet.cell_value(i, 4), composition=worksheet.cell_value(i, 5),
                                                    image=f"image_large/{worksheet.cell_value(i, 6)}")
        new_product.save()
