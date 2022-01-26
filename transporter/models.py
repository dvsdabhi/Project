from django.db import models

# Create your models here.

class Transporter(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    address = models.TextField()
    mobile = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    pic = models.FileField(upload_to='profile',default='download.jpg')


    def __str__(self):
        return self.email