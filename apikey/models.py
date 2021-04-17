from django.db import models

class ApiKeyModel(models.Model):
    key = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "APIKeys"
        