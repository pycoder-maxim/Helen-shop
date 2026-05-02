from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created', 'status', 'is_paid', 'paid_at', 'get_total_cost']
    list_filter = ['status', 'is_paid', 'created']
    list_editable = ['status']
    search_fields = ['user__username', 'first_name', 'last_name', 'email']
    readonly_fields = ['created', 'updated', 'paid_at']
    inlines = [OrderItemInline]

    def get_total_cost(self, obj):
        return f"{obj.get_total_cost()} ₽"

    get_total_cost.short_description = 'Общая стоимость'

    # Добавляем иконки для наглядности
    def is_paid(self, obj):
        if obj.is_paid:
            return '✅ Оплачен'
        return '❌ Не оплачен'

    is_paid.short_description = 'Статус оплаты'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']
    list_filter = ['order__status']
    search_fields = ['product__name', 'order__user__username']
