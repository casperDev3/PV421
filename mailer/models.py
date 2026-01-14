from django.db import models

# Create your models here.
class Mailer(models.Model):
    message = models.TextField()
    status = models.TextField()
    progress = models.IntegerField()

    def __str__(self):
        return self.subject
