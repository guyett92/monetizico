from django.db import models
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from django_s3_storage.storage import S3Storage

storage = S3Storage(aws_s3_bucket_name='exchange-2')


# Create your models here.

# Can reorder or make more
TAGS = (
    ('A', 'Animals'),
    ('V', 'Vehicles'),
    ('H', 'Household Goods'),
    ('F', 'Furniture'),
    ('E', 'Electronics'),
    ('C', 'Clothes'),
    ('J', 'Jewelry'),
    ('M', 'Makeup'),
    ('B', 'Books'),
    ('S', 'Sports'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True)
    avatar = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

class Product(models.Model):
    description = models.TextField(max_length=1000)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    tag = models.CharField(max_length=1, choices=TAGS, default=TAGS[0][0])
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=storage)

    def get_absolute_url(self):
        return reverse('AddPost')
    
    def __str__(self):
        return self.name

class Post(models.Model):
    exp_date = models.DateField(default=(date.today()+timedelta(days=30)).isoformat()) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return reverse('home')

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post)
    # total = calculated from price in Product model; or do it in the view

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)

# class Reviews(models.Model):
#     ICEBOX