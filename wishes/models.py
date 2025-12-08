from django.db import models

class Wish(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_bought = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def __to__dict__(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'is_bought': self.is_bought
        }
