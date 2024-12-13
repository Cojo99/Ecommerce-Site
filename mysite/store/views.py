from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem
from django.core.paginator import Paginator
from django.conf import settings
import stripe
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from .serializers import ProductSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def home(request):
    product_obj = Product.objects.all()
    return render(request, 'store/home.html', {'product_obj': product_obj}) #, {'products': products}


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AllViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



def product_list(request):
    # Get all products initially
    product_obj = Product.objects.all()

    # Handle search by product name
    product_name = request.GET.get('product_name')
    if product_name:
        product_obj = product_obj.filter(name__icontains=product_name)

    # Handle filter by gender
    gender = request.GET.get('gender')
    if gender:
        product_obj = product_obj.filter(gender=gender)

    # Handle filter by category
    category = request.GET.get('category')
    if category:
        product_obj = product_obj.filter(category=category)

    # Pagination setup
    paginator = Paginator(product_obj, 12)  # 12 products per page
    page = request.GET.get('page')
    product_obj = paginator.get_page(page)

    return render(request, 'store/product_list.html', {'product_obj': product_obj})


    # product_obj = Product.objects.all()

    # product_name = request.GET.get('product_name')
    # if product_name != '' and product_name is not None:
    #     product_obj = product_obj.filter(name__icontains=product_name)

    # paginator = Paginator(product_obj, 12)
    # page = request.GET.get('page') #get from the url
    # product_obj = paginator.get_page(page) # page is from above line

    # return render(request, 'store/product_list.html', {'product_obj': product_obj})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def cart(request):
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            item.subtotal = (item.quantity or 0) * (item.product.price or 0)
        
        total = sum(item.subtotal for item in cart_items)
    else:
        session_id = request.session.session_key or request.session.create()
        cart_items = CartItem.objects.filter(session_id=session_id)
        
        cart_items = [
            {
                "product": item.product,
                "quantity": item.quantity,
                "total": (item.product.price or 0) * (item.quantity or 0),
            }
            for item in cart_items
        ]
        
        total = sum(item["subtotal"] for item in cart_items)
    
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total})

def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size')

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product, quantity=quantity, size=size)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart_item, created = CartItem.objects.get_or_create(session_id=session_id, product=product, quantity=quantity, size=size)
    
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

def checkout(request):
    # Placeholder for Stripe integration
    return render(request, 'store/checkout.html')


def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    else:
        session_id = request.session.session_key or request.session.create()
        cart_item = get_object_or_404(CartItem, id=item_id, session_id=session_id)

    cart_item.delete()

    return redirect('cart')


# Checkout page

def checkout(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_id = request.session.session_key or request.session.create()
        cart_items = CartItem.objects.filter(session_id=session_id)

    if not cart_items:
        # Redirect to cart if no items exist
        return redirect('cart')
    
    line_items = []
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd', 
                'product_data': {
                    'name': item.product.name,
                    'description': f"Size: {item.size}" if item.size else "No size selected",
                },
                'unit_amount': int(item.product.price * 100), 
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://127.0.0.1:8000/success',  # might need to replace with your own local address
        cancel_url='http://127.0.0.1:8000/cancel',   # might need to replace with your own local address
    )

    return redirect(session.url)

def success(request):

    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user).delete()
    else:
        session_id = request.session.session_key
        if session_id:
            CartItem.objects.filter(session_id=session_id).delete()

    return render(request, 'store/success.html')

def cancel(request):
    return render(request, 'store/cancel.html')


class MensView(viewsets.ModelViewSet):
    queryset = Product.objects.filter(gender="Mens's")
    serializer_class = ProductSerializer

class WomensView(viewsets.ModelViewSet):
    queryset = Product.objects.filter(gender="Women's")
    serializer_class = ProductSerializer

class ShortsView(viewsets.ModelViewSet):
    queryset = Product.objects.filter(category='Shorts')
    serializer_class = ProductSerializer

class ShirtsView(viewsets.ModelViewSet):
    queryset = Product.objects.filter(category='Shirts')
    serializer_class = ProductSerializer