from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('posts/<int:post_id>/add_photo', views.add_photo, name='add_photo'),
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
]