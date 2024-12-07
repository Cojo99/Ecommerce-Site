from django.shortcuts import render, redirect
from .models import Product, CartItem
from django.core.paginator import Paginator



# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html') #, {'products': products}





def product_list(request):
    product_obj = Product.objects.all()

    product_name = request.GET.get('product_name')
    if product_name != '' and product_name is not None:
        product_obj = product_obj.filter(name__icontains=product_name)

    paginator = Paginator(product_obj, 6) # display 3 items
    page = request.GET.get('page') #get from the url
    product_obj = paginator.get_page(page) # page is from above line

    return render(request, 'store/product_list.html', {'product_obj': product_obj})




def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_id = request.session.session_key
        cart_items = CartItem.objects.filter(session_id=session_id)

    total = sum(item.quantity * item.product.price for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size')

    if request.user.is_authenticated:
        CartItem.objects.create(user=request.user, product=product, quantity=quantity, size=size)
    else:
        session_id = request.session.session_key or request.session.create()
        CartItem.objects.create(session_id=session_id, product=product, quantity=quantity, size=size)

    return redirect('cart')

def checkout(request):
    # Placeholder for Stripe integration
    return render(request, 'store/checkout.html')