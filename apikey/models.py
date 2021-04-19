from django.db import models

class ApiKeyModel(models.Model):
    """
    Model to store API keys.
    """
    key = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "APIKeys"
        