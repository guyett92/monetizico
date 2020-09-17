from django.db import models
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True)
    avatar = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Product(models.Model):
    description = models.TextField(max_length=1000)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    tag = models.CharField(max_length=25)

class Post(models.Model):
    exp_date = models.DateField(default=(date.today()+timedelta(days=30)).isoformat()) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    # total = calculated from price in Product model; or do it in the view

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)

class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)

# class Reviews(models.Model):
#     ICEBOX