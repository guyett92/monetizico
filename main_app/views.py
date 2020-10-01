from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from botocore.exceptions import ClientError
from django.dispatch import receiver
from django.contrib.postgres.search import SearchQuery
from .models import Product, Cart, Post, User
from .forms import ProfileForm, UserForm, ContactForm
from datetime import date, timedelta
import uuid
import boto3
import stripe
import environ
import json
import math

env = environ.Env()
environ.Env.read_env()

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

# Create your views here

# Define the home view
def home(request):
  posts = Post.objects.filter(active=True)

  def get_post_status(request):
    all_posts = Post.objects.all()
    for post in all_posts:
      if date.today() > post.exp_date:
        post.active = False
        post.save()
  return render(request, 'home.html', {'posts': posts})

class AddProduct(LoginRequiredMixin, CreateView):
  model = Product
  fields = ['name', 'price','description', 'tag', 'quantity', 'photo']

  def form_valid(self, form):
    form.instance.seller = self.request.user
    return super().form_valid(form)
    
class UpdateProduct(LoginRequiredMixin, UpdateView):
  model = Product
  fields = ['name', 'description', 'price', 'tag', 'quantity', 'photo']
  
class DeleteProduct(LoginRequiredMixin, DeleteView):
  model = Product
  success_url = '/'

def delete_product(request):
  Product.objects.filter(id=request.POST['product_id']).delete()
  return render(request, 'home.html')

class PostDetail(DetailView):
  model = Post

    
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

  
class DeletePost(LoginRequiredMixin, DeleteView):
  model = Post
  success_url = '/'

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
            return redirect('home') #FIXME: redirect to profile page
    else:
            user_form = UserForm()
            profile_form = ProfileForm()
            messages.error(request, ('Please correct the error below.'))
    return render(request, 'registration/register.html', {
            'user_form': user_form,
            'profile_form': profile_form
    })

def cart(request):
  return render(request, 'cart.html')

def create_cart(request, post_id):
  cart = Cart(user=request.user)
  cart.save()
  cart.posts.add(post_id)
  cart.save()
  return redirect('cart')

def add_to_cart(request, cart_id, post_id):
  Cart.objects.get(id=cart_id).posts.add(post_id)
  return redirect('cart')
  
def remove_from_cart(request, cart_id, post_id):
  Cart.objects.get(id=cart_id).posts.remove(post_id)
  return redirect('cart')

@csrf_exempt
def stripe_config(request):
  if request.method == 'GET':
    stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
    return JsonResponse(stripe_config, safe=False)

def get_products(products):
  lst1 = []
  for product in products:
    posts = product.posts.all()
    for post in posts:
      if post.active:
        item = {
          'name': post.product.name,
          'quantity': post.product.quantity,
          'currency': 'usd',
          'amount': int(math.floor(post.product.price) * 100), #multiply by 100 d/t doesn't recognize decimal
        }
        lst1.append(item)
  return lst1

@csrf_exempt
def create_checkout_session(request):
  if request.method == 'GET':
    domain_url = 'http://localhost:8000/'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
      products = Cart.objects.filter(user=request.user)
      checkout_session = stripe.checkout.Session.create(
        success_url = domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url = domain_url + 'cancelled/',
        payment_method_types = ['card'],
        mode = 'payment',
        line_items = get_products(products),
        metadata = { 'user': request.user }
      )
      return JsonResponse({'sessionId': checkout_session['id']})
    except Exception as e:
      return JsonResponse({'error': str(e)})

@csrf_exempt
def stripe_webhook(request):
  stripe.api_key = settings.STRIPE_SECRET_KEY
  endpoint_secret = env('STRIPE_ENDPOINT_SECRET')
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)
  
  if event['type'] == 'checkout.session.completed':
    print("Payment was successful")
    print(payload)
    
    # set posts to inactive
    user = payload.decode('UTF-8').split('"user": ')[1].split('"')[1]
    user_id = User.objects.filter(username=user)[0].id
    products = Cart.objects.filter(user=user_id)
    for product in products:
      print(product)
      posts = product.posts.all()
      print(posts)
      for post in posts:
        print(post.active)
        post.active = False
        print(post.active)
        post.save()
  return HttpResponse(status=200)

def success(request):
  return render(request, 'success.html')

def cancelled(request):
  return render(request, 'cancelled.html')

##Django Email
def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('successemail')
    return render(request, "email.html", {'form': form})

def successView(request):
    return render(request, 'successemail.html')
  
class SearchResultsView(ListView):
  model = Post

  def get_queryset(self):
    query = self.request.GET.get('q')
    post_list = Post.objects.filter(product__name__icontains=query)
    return post_list

class TagSearchView(ListView):
  model = Post

  def get_queryset(self):
    query = self.request.GET.get('q')
    post_list = Post.objects.filter(product__tag=query)
    return post_list