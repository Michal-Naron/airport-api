from django.db import models

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

