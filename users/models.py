from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):

        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    orders = models.ManyToManyField("products.Order", verbose_name="Заказы", related_name="user", blank=True)
    cakes = models.ManyToManyField("mainapp.Cake", verbose_name="Заказы тортов", related_name="user", blank=True)
    cart = models.OneToOneField("products.Cart", verbose_name="Корзина", related_name="user", on_delete=models.SET_NULL, blank=True, null=True)

    full_name = models.CharField(verbose_name="ФИО", max_length=100, blank=True, null=True)
    email = models.EmailField(verbose_name="Почта", unique=True)
    phone = models.CharField(verbose_name="Номер телефона", max_length=20, blank=True, null=True)
    date_reg = models.DateTimeField(verbose_name="Дата регистрации", auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin