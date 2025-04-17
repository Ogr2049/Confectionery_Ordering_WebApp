from django.db import models
from utils.utils import russian_to_engilsh

class Receipt(models.Model):

    author = models.ForeignKey("users.User", verbose_name="Автор", on_delete=models.SET_NULL, related_name="receipts", blank=True, null=True)
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    cover = models.ImageField(verbose_name="Обложка", blank=True, null=True)
    likes = models.IntegerField(verbose_name="Лайки", default=0)
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(max_length=200, blank=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = russian_to_engilsh(self.title)
        super(Receipt, self).save(*args, **kwargs)

    class Meta:
        verbose_name="Рецепт"
        verbose_name_plural="Рецепты"


