from datetime import datetime

from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import ValidationError

from apps.order.models import Order, Table


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ["id", "number", "capacity"]


class OrderSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d-%m-%Y", input_formats=["%d-%m-%Y"])

    def validate_format(self, value):
        """
        Validation date format
        """
        if value != datetime.strptime(value, "%d-%m-%Y").date():
            raise ValidationError("Invalid date format. Please use the format 'dd-mm-yyyy'.")
        return value

    def validate_date(self, value):
        """
        Validation date on yesterday day
        """
        if value < timezone.now().date():
            raise ValidationError("Date cannot be in the past.")
        return value

    class Meta:
        model = Order
        fields = ["id", "date", "customer_name", "customer_email"]


class AvailableTablesSerializer(OrderSerializer):
    class Meta(OrderSerializer.Meta):
        fields = ["id", "date"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("customer_name", None)
        self.fields.pop("customer_email", None)
