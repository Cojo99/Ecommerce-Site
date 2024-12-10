from django.shortcuts import render, redirect
from .models import Product, CartItem
from django.core.paginator import Paginator

from rest_framework import viewsets
from .serializers import ProductSerializer


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
    product_obj = Product.objects.all()

    product_name = request.GET.get('product_name')
    if product_name != '' and product_name is not None:
        product_obj = product_obj.filter(name__icontains=product_name)

    paginator = Paginator(product_obj, 12)
    page = request.GET.get('page') #get from the url
    product_obj = paginator.get_page(page) # page is from above line

    return render(request, 'store/product_list.html', {'product_obj': product_obj})


["S", "M", "L","XL"]

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

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