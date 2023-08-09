from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    general = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(upload_to="uploads/", null=True, blank=True)
    coverPhoto = models.ImageField(upload_to="uploads/", null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.CharField(max_length=50, primary_key=True, auto_created=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    photo = models.ImageField(upload_to="uploads/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    dateAdded = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    available = models.IntegerField()

    def __str__(self):
        return str(self.product)


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Shopping cart " + self.user


class CartProducts(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Wishlist " + self.user


class WishlistProduct(models.Model):
    wish = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cart_product = models.ForeignKey(CartProducts, on_delete=models.CASCADE, null=True)

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    totalPaid = models.IntegerField()
    dateCreated = models.DateTimeField()
    status = models.CharField(max_length=100)

class OrderHistoryItem(models.Model):
    history = models.ForeignKey(OrderHistory, on_delete=models.CASCADE)
    item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Delivery(models.Model):
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    email = models.EmailField()