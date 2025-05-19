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


