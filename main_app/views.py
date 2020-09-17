from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Cart, Photo, Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from botocore.exceptions import ClientError
import uuid
import boto3

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
  pass 

def user_profile(get):
  pass

def update_user_profile():
  pass

def delete_user_profile():
  pass

def register():
  error_message = ''
  if request.method == 'POST':
        #creae a user form object that includes data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
            #adding user to db
        user = form.save()
        login(request, user)
        return redirect('index')
  else: 
      error_message = 'Invalid sign up, try again!'
            #either bad POT request or a GET reqeust so just render the empty form
  form = UserCreationForm()
  context = { 'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

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

