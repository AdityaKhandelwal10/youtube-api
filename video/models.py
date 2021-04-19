from django.db import models

class VideoModel(models.Model):
    """
    Creates a database model in the backgroud for storing video details
    """
    vid_id = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length =144)
    desc = models.TextField()
    published_date = models.DateTimeField()
    thumbnail_url = models.URLField()

    class Meta:
        verbose_name_plural= 'Videos'
    
    def __str__(self):
        return self.title