from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published', default=datetime.now)
    image = models.ImageField(upload_to='images', null=True, blank=True)
