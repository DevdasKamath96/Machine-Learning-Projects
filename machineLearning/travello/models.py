from django.db import models


class Destination(models.Model):

    name = models.CharField(max_length=50)
    descr = models.TextField()
    price = models.IntegerField()
    img = models.ImageField(upload_to = 'pics')
    offer = models.BooleanField(default=False)

