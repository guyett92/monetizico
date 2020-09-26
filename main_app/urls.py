from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('cart/', views.cart, name='cart'),
    path('config/', views.stripe_config, name='config'),
    path('create-checkout-session/', views.create_checkout_session, name='checkout-session'),
    path('success/', views.success, name='success'),
    path('cancelled/', views.cancelled, name='cancelled'),
    path('products/create', views.AddProduct.as_view(), name='AddProduct'),
    path('products/<int:pk>/update', views.UpdateProduct.as_view(), name='UpdateProduct'),
    path('products/<int:pk>/delete', views.DeleteProduct.as_view(), name='DeleteProduct'),
    path('posts/create', views.AddPost.as_view(), name='AddPost'),
    path('posts/<int:pk>/update', views.UpdatePost.as_view(), name='UpdatePost'),
    path('posts/<int:pk>/delete', views.DeletePost.as_view(), name='DeletePost'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    # path('posts/<int:post_id>', views.post_detail, name='post_detail'),
    path('carts/<int:post_id>/create', views.create_cart, name='create_cart'),
    path('carts/<int:cart_id>/add_to_cart/<int:post_id>', views.add_to_cart, name='add_to_cart'),
    path('carts/<int:cart_id>/remove_from_cart/<int:post_id>', views.remove_from_cart, name='remove_from_cart'),
    path('webhook/', views.stripe_webhook),
]