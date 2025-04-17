# Generated by Django 5.2 on 2025-04-14 15:13

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('total_price', models.FloatField(default=0, verbose_name='Конечная цена')),
            ],
            options={
                'verbose_name': 'Продукт в корзине',
                'verbose_name_plural': 'Продукты в корзине',
            },
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Полный адрес')),
                ('pickup', models.BooleanField(default=False, verbose_name='Cамовывоз')),
            ],
            options={
                'verbose_name': 'Доставка',
                'verbose_name_plural': 'Доставки',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_all', models.PositiveIntegerField(default=0, verbose_name='Общее кол-во товаров')),
                ('total_price', models.FloatField(default=0, verbose_name='Цена корзины')),
                ('cart_products', models.ManyToManyField(blank=True, related_name='cart', to='products.cartproduct', verbose_name='Продукты в корзине')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=200, verbose_name='URL')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Изображение')),
                ('show_main', models.BooleanField(default=False, verbose_name='Разместить на главной')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category', verbose_name='Родитель')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, default='В процессе', max_length=50, null=True, verbose_name='Статус заказа')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='ФИО')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Почта')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона')),
                ('type_pay', models.CharField(blank=True, choices=[('online', 'Оплата онлайн на сайте'), ('cash', 'Наличными при получении'), ('card', 'Картой при получении')], max_length=70, null=True, verbose_name='Способ оплаты')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('quantity_all', models.PositiveBigIntegerField(default=1, verbose_name='Кол-во товаров')),
                ('amount', models.FloatField(default=1, verbose_name='Цена заказа')),
                ('date_order', models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')),
                ('delivery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='products.delivery', verbose_name='Доставка')),
                ('products', models.ManyToManyField(blank=True, related_name='orders', to='products.cartproduct', verbose_name='Продукты')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, verbose_name='URL')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name='Вес')),
                ('composition', models.TextField(blank=True, null=True, verbose_name='Состав')),
                ('date_add', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время добавления')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to='products.product'),
        ),
    ]
