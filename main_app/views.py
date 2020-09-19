from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Cart, Photo, Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from botocore.exceptions import ClientError
import uuid
import boto3
from django.dispatch import receiver
from .forms import ProfileForm, UserForm
from .models import User

#S3_BASE_URL = ""
#BUCKET = ""
# Create your views here

# Define the home view
def home(request):
  return render(request, 'home.html')

def product_detail(request, product_id):
  pass

def product(get):
  pass

def add_product_post(post):
  pass

def delete_product_post():
  pass

def update_product_post():
  pass

def about(request):
  return render(request, 'about.html') 

def profile(request):
  return render(request, 'profile.html') 

def update_profile():
  pass

def delete_profile():
  pass


def register(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid() and user_form.cleaned_data['password'] == user_form.cleaned_data['password_confirm']:
            user = User.objects.create_user(
              username = user_form.cleaned_data['username'],
              email = user_form.cleaned_data['email'],
              password = user_form.cleaned_data['password'],
              first_name = user_form.cleaned_data['first_name'],
              last_name = user_form.cleaned_data['last_name']
            )
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            #login(request, user)
            messages.success(request, f"Your profile was successfully created!")
            return redirect('home') #fix me
    else:
            user_form = UserForm()
            profile_form = ProfileForm()
            messages.error(request, ('Please correct the error below.'))
    return render(request, 'register.html', { #fix me redirect to registration page
            'user_form': user_form,
            'profile_form': profile_form
    })

def add_photo():
  pass

def update_photo():
  pass

def delete_photo():
  pass

def add_to_cart():
  pass

def remove_from_cart():
  pass 

