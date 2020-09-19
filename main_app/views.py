from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Product, Cart, Photo, Post, User
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
import stripe
from django.dispatch import receiver
from .forms import ProfileForm, UserForm

#S3_BASE_URL = ""
#BUCKET = ""
# Create your views here

# Define the home view
def home(request):
  return render(request, 'home.html')

class AddProduct(LoginRequiredMixin, CreateView):
  model = Product
  fields = ['name', 'price','description', 'tag']

  def form_valid(self, form):
    form.instance.seller = self.request.user
    return super().form_valid(form)
    
def update_product():
  pass

def delete_product():
  pass

def post_detail(request, post_id):
  pass

class post_index():
  pass

class AddPost(LoginRequiredMixin, CreateView):
  model = Post
  fields = ['product']
  
  def get_form(self, form_class=None):
    form = super().get_form(form_class=None)
    form.fields['product'].queryset = form.fields['product'].queryset.filter(seller = self.request.user)
    return form
    
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

def update_post():
  pass

def delete_post():
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
            login(request, user)
            messages.success(request, f"Your profile was successfully created!")
            return redirect('home') #fix me
    else:
            user_form = UserForm()
            profile_form = ProfileForm()
            messages.error(request, ('Please correct the error below.'))
    return render(request, 'registration/register.html', { #fix me redirect to registration page
            'user_form': user_form,
            'profile_form': profile_form
    })

def add_photo():
  pass

def update_photo():
  pass

def delete_photo():
  pass

def cart(request):
  return render(request, 'cart.html')

def add_to_cart():
  pass

def remove_from_cart():
  pass 

@csrf_exempt
def stripe_config(request):
  if request.method == 'GET':
    stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
    return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
  if request.method == 'GET':
    domain_url = 'http://localhost:8000/'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
      product = Product.objects.get(id=2)
      checkout_session = stripe.checkout.Session.create(
        success_url = domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url = domain_url + 'cancelled/',
        payment_method_types = ['card'],
        mode = 'payment',
        line_items = [
          {
            'name': product.name,
            'quantity': 1,
            'currency': 'usd',
            'amount': product.price * 100, #multiply by 100 d/t doesn't recognize decimal
          }
        ]
      )
      return JsonResponse({'sessionId': checkout_session['id']})
    except Exception as e:
      return JsonResponse({'error': str(e)})

def success(request):
  return render(request, 'success.html')

def cancelled(request):
  return render(request, 'cancelled.html')
