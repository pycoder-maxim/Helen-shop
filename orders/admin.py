from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created', 'status', 'get_total_cost']
    list_filter = ['status', 'created']
    list_editable = ['status']
    search_fields = ['user__username', 'first_name', 'last_name', 'email']
    readonly_fields = ['created', 'updated']
    inlines = [OrderItemInline]

    def get_total_cost(self, obj):
        return f"{obj.get_total_cost()} ₽"

    get_total_cost.short_description = 'Общая стоимость'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']
    list_filter = ['order__status']
    search_fields = ['product__name', 'order__user__username']
