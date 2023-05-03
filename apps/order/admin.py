from django.contrib import admin

from apps.order.models import Order, Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "capacity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "table", "date", "customer_name", "customer_email")
