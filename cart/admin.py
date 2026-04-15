from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_items', 'get_total_price', 'created']
    inlines = [CartItemInline]

    def get_total_items(self, obj):
        return obj.get_total_items()

    get_total_items.short_description = 'Всего товаров'

    def get_total_price(self, obj):
        return f"{obj.get_total_price()} ₽"

    get_total_price.short_description = 'Общая стоимость'
