from rest_framework import serializers

from apps.order.models import Order, Table


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ["id", "number", "capacity"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "date", "customer_name", "customer_email"]
