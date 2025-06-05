from django.db import models
from utils.utils import russian_to_engilsh
from django.db import models

class Category(models.Model):

    title = models.CharField(max_length=150,verbose_name='Название')
    slug = models.SlugField(max_length=200,blank=True,verbose_name='URL')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = russian_to_engilsh(self.title)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

class Product(models.Model):

    title = models.CharField(max_length=150,verbose_name='Название')
    slug = models.SlugField(max_length=200,blank=True,null=True,verbose_name='URL')
    description = models.TextField(blank=True,null=True,verbose_name='Описание')
    image = models.ImageField(blank=True,null=True,verbose_name='Изображение')
    price = models.FloatField(verbose_name='Цена', blank=True, null=True)
    weight = models.CharField(verbose_name="Вес", blank=True, null=True, max_length=100)
    composition = models.TextField(verbose_name="Состав", blank=True, null=True)

    category = models.ForeignKey(to=Category,on_delete=models.CASCADE,verbose_name='Категория', blank=True, null=True, related_name="products")

    date_add = models.DateTimeField(verbose_name="Время добавления", blank=True, null=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = russian_to_engilsh(self.title)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, related_name="cart_products")
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=1)
    total_price = models.FloatField(verbose_name="Конечная цена", default=0)

    def __str__(self):
        return f"{self.product.title} | {self.quantity} шт."

    class Meta:
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзине"


class Cart(models.Model):
    cart_products = models.ManyToManyField(CartProduct, verbose_name="Продукты в корзине", blank=True,
                                           related_name="cart")
    quantity_all = models.PositiveIntegerField(verbose_name="Общее кол-во товаров", default=0)
    total_price = models.FloatField(verbose_name="Цена корзины", default=0)

    def __str__(self):
        return f"Корзина №{self.id}"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


TYPE_PAY = (
    ("online", "Оплата онлайн"),
    ("cash", "Оплата при получении"),
)


class Delivery(models.Model):

    address = models.CharField(verbose_name="Полный адрес", max_length=200, blank=True, null=True)
    pvz = models.CharField(verbose_name="Пункт выдачи", max_length=200, blank=True, null=True)
    date_delivery = models.CharField(verbose_name="Дата доставки", max_length=20, blank=True, null=True)

    def __str__(self):
        if self.address:
            return f"Доставка на {self.address}"
        return f"Доставка - {self.pvz} (Пункт выдачи)"

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"


class Order(models.Model):

    status = models.CharField(verbose_name="Статус заказа", max_length=50, default="В процессе",
                              blank=True, null=True)
    full_name = models.CharField(verbose_name="ФИО", max_length=100, blank=True, null=True)
    email = models.EmailField(verbose_name="Почта", blank=True, null=True)
    phone = models.CharField(verbose_name="Номер телефона", max_length=20, blank=True, null=True)
    type_pay = models.CharField(verbose_name="Способ оплаты", choices=TYPE_PAY, max_length=70, blank=True, null=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    delivery = models.ForeignKey(Delivery, verbose_name="Доставка", on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name="order")
    products = models.ManyToManyField(CartProduct, verbose_name="Продукты", blank=True, related_name="orders")
    quantity_all = models.PositiveBigIntegerField(verbose_name="Кол-во товаров", default=1)
    amount = models.FloatField(verbose_name="Цена заказа", default=1)

    date_order = models.DateTimeField(verbose_name="Дата заказа", auto_now_add=True)

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
