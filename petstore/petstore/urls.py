"""
URL configuration for petstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from store.views import home, register_view, \
    login_view, categories, category_detail, logout_view,\
    add_to_wishlist, wishlist, shopping_cart, add_to_shopping_cart, update_quantity, place_order, delivery, history

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name="home"),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('categories/<str:category_name>/<str:subcategory_name>/', category_detail, name='category_detail'),
    path('categories/<str:category_name>/<str:subcategory_name>/', category_detail, name='category_detail'),
    path('categories/<str:category_name>/', category_detail, name='category_detail'),
    path('categories/', categories, name='categories'),
    path('addToWishlist/<int:product_id>/', add_to_wishlist, name='wishlistAdd'),
    path('wishlist/<int:product_id>/', wishlist, name='wishlist'),
    path('wishlist/', wishlist, name='wishlist'),
    path('shoppingCartAdd/<int:product_id>', add_to_shopping_cart, name='shopping_cart_add'),
    path('shoppingCart/<int:product_id>', shopping_cart, name='shopping_cart'),
    path('shoppingCart/', shopping_cart, name='shopping_cart'),
    path('update_quantity/<int:product_id>/', update_quantity, name='update_quantity'),
    path('order/', place_order, name='place_order'),
    path('delivery/', delivery, name='delivery',),
    path('myOrders/', history, name='myorders',),
    path('logout/', logout_view, name='logout'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
