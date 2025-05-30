from django.db import models
from utils.utils import russian_to_engilsh

class Like(models.Model):

    user = models.ForeignKey("users.User", verbose_name="User", on_delete=models.SET_NULL, related_name="likes",
                               blank=True, null=True)

    class Meta:
        verbose_name="Лайк"
        verbose_name_plural="Лайки"

class Receipt(models.Model):

    author = models.ForeignKey("users.User", verbose_name="Автор", on_delete=models.SET_NULL, related_name="receipts", blank=True, null=True)
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    cover = models.ImageField(verbose_name="Обложка", blank=True, null=True)
    likes = models.ManyToManyField(Like, verbose_name="Лайки", default=0, related_name="receipt")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(max_length=200, blank=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{russian_to_engilsh(self.title)}-{self.id}"
        super(Receipt, self).save(*args, **kwargs)

    class Meta:
        verbose_name="Рецепт"
        verbose_name_plural="Рецепты"


class CategoryIngredient(models.Model):

    title = models.CharField(verbose_name="Название", max_length=200)
    slug = models.CharField(verbose_name="Slug", max_length=220, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Категория Ингредиента"
        verbose_name_plural="Категории Ингредиентов"

class Ingredient(models.Model):

    title = models.CharField(verbose_name="Название", max_length=200)
    category = models.ForeignKey(CategoryIngredient, verbose_name="Категория", on_delete=models.SET_NULL, blank=True, null=True, related_name="ingredients")
    cover = models.ImageField(verbose_name="Обложка", blank=True, null=True)
    price = models.IntegerField(verbose_name="Цена", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Ингредиент"
        verbose_name_plural="Ингредиенты"