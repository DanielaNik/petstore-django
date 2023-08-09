from django.contrib import admin

from .models import Product, Category, ProductItem, Order, ShoppingCart, OrderItems, CartProducts, Wishlist, \
    WishlistProduct, OrderHistory, OrderHistoryItem


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj:Product | None = None):
        if obj is not None and request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj:Product | None = None):
        if obj is not None and request.user.is_superuser:
            return True
        return False


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj:Category | None = None):
        if obj is not None and request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj:Category | None = None):
        if obj is not None and request.user.is_superuser:
            return True
        return False


admin.site.register(Category, CategoryAdmin)


class ProductItemAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj:ProductItem | None = None):
        if obj is not None and request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj:ProductItem | None = None):
        if obj is not None and request.user.is_superuser:
            return True
        return False


admin.site.register(ProductItem, ProductItemAdmin)

admin.site.register(Order)
admin.site.register(ShoppingCart)
admin.site.register(OrderItems)
admin.site.register(CartProducts)
admin.site.register(Wishlist)
admin.site.register(WishlistProduct)
admin.site.register(OrderHistory)
admin.site.register(OrderHistoryItem)