from django import template
from ..models import Product, Cart

register = template.Library()

@register.filter
def product_count(user):
    products = Product.objects.filter(seller=user.id)
    if products:
        return True
    return False

@register.simple_tag
def get_products(user):
    return Product.objects.filter(seller=user.id)

@register.simple_tag
def get_cart(user):
    return Cart.objects.filter(user=user.id)

@register.simple_tag
def get_posts(user):
    posts = []
    cart = Cart.objects.filter(user=user.id)
    for product in cart:
        for post in product.posts.all():
            if post.active:
                posts.append(post)
    return posts

@register.simple_tag
def get_total(posts):
    total = 0.00
    for post in posts:
        total += post.product.quantity * post.product.price
    return "%.2f" % total