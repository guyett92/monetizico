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

def about():
  return render(request, 'about.html') 

def profile(get):
  pass

def update_profile():
  pass

def delete_profile():
  pass

def registration_form(request):
  return render(request, 'register.html') 

def register(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user_profile = profile_form.save(commit=False)
            user_profile.user = user 
            user_profile.save()
            #login(request, user)
            messages.success(request, f"Your profile was successfully created!")
            return redirect('home') #fix me
    else:
            user_form = UserForm(request.POST)
            profile_form = ProfileForm(request.POST)
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

