"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from store.views import home, product_list, product_detail, cart
from store.views import add_to_cart, checkout, remove_from_cart, success, cancel
from store.views import MensView, WomensView, ShirtsView, ShortsView
from users import views as user_views
from django.contrib.auth import views as authentication_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    # path('products/<str:category>/<str:gender>/', product_list, name='product_list'),
    path('products/', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('cart/', cart, name='cart'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('users/', include('users.urls')),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),

    path('products/mens/', MensView.as_view({'get': 'list'}), name='mens_products'),
    path('products/womens/', WomensView.as_view({'get': 'list'}), name='womens_products'),
    path('products/shorts/', ShortsView.as_view({'get': 'list'}), name='shorts_products'),
    path('products/shirts/', ShirtsView.as_view({'get': 'list'}), name='shirts_products'),

    path('register/', user_views.register, name='register'),
    path('login/', authentication_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', authentication_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profilepage, name='profile')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
