from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import Category, Product, Wishlist, WishlistProduct, ShoppingCart, CartProducts, ProductItem, Order, \
    OrderItems, OrderHistory, OrderHistoryItem
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm, DeliveryForm
from django.db.models import Count


# Create your views here.
def home(request):
    categories = Category.objects.filter(general=None)
    sub_categories = Category.objects.exclude(general=None)
    products = Product.objects.order_by('-dateAdded')[:3]
    context = {"main_categories": categories, "sub_categories": sub_categories, "products": products}
    return render(request, "homepage.html", context=context)


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Log in the user after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Redirect to the home page or any other page
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page or any other page
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def categories(request):
    main_categories = Category.objects.filter(general=None)
    sub_categories = Category.objects.exclude(general=None)
    context = {
        "main_categories": main_categories,
        "sub_categories": sub_categories,
    }
    return render(request, "categories.html", context=context)


def category_detail(request, category_name, subcategory_name=None):
    sort_option = request.GET.get('sort', None)
    if sort_option == 'highest':
        sort_field = '-price'  # Sort by price in descending order (highest first)
    elif sort_option == 'lowest':
        sort_field = 'price'  # Sort by price in ascending order (lowest first)
    else:
        sort_field = 'name'  # Default sorting option (e.g., sort by name)

    main_categories = Category.objects.filter(general=None)
    sub_categories = Category.objects.exclude(general=None)
    try:
        main_category = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        return redirect('home')

    if subcategory_name:
        products = Product.objects.filter(category__name=subcategory_name, category__general__name=category_name)
    else:
        products = Product.objects.filter(category__general__name=category_name, category__in=sub_categories)

    products = products.order_by(sort_field)
    context = {
        'category_name': category_name,
        'subcategory_name': subcategory_name,
        'products': products,
        "main_categories": main_categories,
        "sub_categories": sub_categories,
        "category": main_category,
    }
    return render(request, 'category_detail.html', context=context)


def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        product = Product.objects.get(id=product_id)

        if WishlistProduct.objects.filter(wish=wishlist, item=product).exists():
            pass
        else:
            wishlist_product = WishlistProduct.objects.create(wish=wishlist, item=product)

        return redirect(request.META.get('HTTP_REFERER', reverse('home')) + '?show_toast_wishlist=true')


def find_top_categories(wishlist_id, n):
    top_categories = (
        Product.objects.filter(wishlistproduct__wish=wishlist_id)
        .values('category')
        .annotate(count=Count('category'))
        .order_by('-count')[:n]
    )

    return [category['category'] for category in top_categories]


def wishlist(request, product_id=None):
    main_categories = Category.objects.filter(general=None)
    sub_categories = Category.objects.exclude(general=None)
    wishlist_user = Wishlist.objects.get(user=request.user)
    wishlist_items = WishlistProduct.objects.filter(wish=wishlist_user)
    items = Product.objects.filter(id__in=wishlist_items.values('item'))

    if request.method == 'POST':
        WishlistProduct.objects.filter(wish=wishlist_user, item__id=product_id).delete()
        return redirect('wishlist')

    categories = find_top_categories(wishlist_user, 2)
    suggested = Product.objects.filter(category__in=categories).exclude(id__in=wishlist_items.values('item'))[:3]

    context = {"items": items, "suggested": suggested, "main_categories": main_categories, "sub_categories": sub_categories}
    return render(request, 'wishlist.html', context=context)


def add_to_shopping_cart(request, product_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        cart, created = ShoppingCart.objects.get_or_create(user=request.user)

        product = ProductItem.objects.get(id=product_id)

        if CartProducts.objects.filter(cart=cart, item=product).exists():
            pass
        else:
            cart_product = CartProducts.objects.create(cart=cart, item=product, quantity=1)
            cart_product.save()
            order, created = Order.objects.get_or_create(user=request.user)
            order_item = OrderItems.objects.create(order=order, cart_product=cart_product)
            order_item.save()

        return redirect(request.META.get('HTTP_REFERER', reverse('home')) + '?show_toast_cart=true')


def shopping_cart(request, product_id=None):
    categories = Category.objects.filter(general=None)
    sub_categories = Category.objects.exclude(general=None)

    cart_user = ShoppingCart.objects.get(user=request.user)
    cart_items = CartProducts.objects.filter(cart=cart_user)
    order = Order.objects.get(user=request.user)
    order_items = OrderItems.objects.filter(order=order).select_related('cart_product__item__product')

    items = CartProducts.objects.filter(cart=cart_user).select_related('item__product')

    if request.method == 'POST':
        product_item = get_object_or_404(CartProducts, item__product__id=product_id, cart=cart_user)
        product_item.delete()
        return redirect('shopping_cart')

    total = 0
    for o in order_items:
        total = total + o.cart_product.quantity * o.cart_product.item.product.price

    context = {"items": items, "order_items": order_items, "total": total, "main_categories": categories, "sub_categories": sub_categories}
    return render(request, 'cart.html', context=context)


def update_quantity(request, product_id):
    if request.method == 'POST':
        cart_user = ShoppingCart.objects.get(user=request.user)
        product_item = get_object_or_404(ProductItem, product__id=product_id, cartproducts__cart=cart_user)
        cart_item = CartProducts.objects.get(cart=cart_user, item=product_item)
        new_quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = new_quantity
        cart_item.save()
    return redirect('shopping_cart')


def delivery(request):
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page or any other page
    else:
        form = DeliveryForm()
    return render(request, 'delivery.html', {'form': form})


def place_order(request):
    if request.method == 'POST':
        cart_user = ShoppingCart.objects.get(user=request.user)
        cart_items = CartProducts.objects.filter(cart=cart_user)
        order = Order.objects.get(user=request.user)
        order_items = OrderItems.objects.filter(order=order).select_related('cart_product__item__product')

        total = 5
        for o in order_items:
            total = total + o.cart_product.quantity * o.cart_product.item.product.price

        order_history = OrderHistory.objects.create(user=request.user, totalPaid=total, dateCreated=timezone.now(),
                                                    status='Created')

        for o in order_items:
            order_history_item = OrderHistoryItem.objects.create(history=order_history, item=o.cart_product.item,
                                                                 quantity=o.cart_product.quantity)

        cart_items.delete()
        return render(request, 'order_successful.html')

    return render(request, 'delivery.html')


def history(request):
    main_categories = Category.objects.filter(general=None)
    sub_categories = Category.objects.exclude(general=None)
    order_history = OrderHistory.objects.filter(user=request.user).order_by('-dateCreated')
    order_history_items = OrderHistoryItem.objects.filter(history__in=order_history).select_related(
        'item__product').all()

    context = {'orders': order_history, 'order_items': order_history_items,
               "main_categories": main_categories, "sub_categories": sub_categories}
    return render(request, 'order_history.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('home')
