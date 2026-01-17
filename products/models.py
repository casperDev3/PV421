from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from sqlalchemy.orm.persistence import post_update


class Product(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Ідентифікатор продукту")
    # add relation to User model
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Користувач")
    # product fields
    name = models.CharField(max_length=255, verbose_name="Назва продукту")
    description = models.TextField(verbose_name="Опис продукту")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна продукту")
    is_available = models.BooleanField(default=True, verbose_name="Доступність продукту")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")



    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"


# _____ SIGNALS FOR PRODUCT MODEL _____ #
# BEFORE CREATE
@receiver(pre_save, sender=Product)
def before_saving_product(sender, instance, **kwargs):
    if instance._state.adding:
        print(f"Перед створенням продукту: {instance.name}")
    else:
        print(f"Перед оновленням продукту: {instance.name}")

# AFTER CREATE
@receiver(post_save, sender=Product)
def after_saving_product(sender, instance, created, **kwargs):
    if created:
        print(f"Продукт створено: {instance.name}")
    else:
        print(f"Продукт оновлено: {instance.name}")

# TODO: Переглянути сигнали для оновлення моделі (перед і після оновлення)
# BEFORE DELETE
@receiver(pre_delete, sender=Product)
def before_deleting_product(sender, instance, **kwargs):
    print(f"Перед видаленням продукту: {instance.name}")

# AFTER  DELETE
@receiver(post_delete,  sender=User)
def after_deleting_product(sender, instance, **kwargs):
    print(f"Продукт видалено: {instance.name}")


