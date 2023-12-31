from django.core.mail import send_mail
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.order.models import Order, Table
from apps.order.serializer import (
    AvailableTablesSerializer,
    OrderSerializer,
    TableSerializer,
)
from config.settings import HOST_EMAIL


class TableViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tables to be viewed or edited.
    """

    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @action(detail=True, methods=["get"])
    def reservations(self, request, pk=None):
        """
        Return a list of reserved dates for a specific table.
        """
        table = get_object_or_404(Table, pk=pk)
        reserved_dates = table.orders.values_list("date", flat=True)
        return Response(reserved_dates)

    @action(detail=False, methods=["get"])
    def available_tables(self, request):
        """
        Return a list of available tables for a specific date.
        """
        serializer = AvailableTablesSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        date = serializer.validated_data["date"]
        available_tables = Table.objects.exclude(orders__date=date)
        serializer = TableSerializer(available_tables, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def occupancy(self, request):
        """
        Return the occupancy percentage for a specific date.
        """
        serializer = AvailableTablesSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        date = serializer.validated_data["date"]
        total_area = Table.objects.aggregate(total_area=Sum(F("width") * F("length")))["total_area"]
        occupied_area = Table.objects.exclude(orders__date=date).aggregate(
            occupied_area=Sum(F("width") * F("length"))
        )["occupied_area"]
        occupancy_percentage = round(occupied_area / total_area * 100, 2)
        return Response(
            {
                "occupancy": occupancy_percentage,
                "total_area": total_area,
                "occupied_area": occupied_area,
            }
        )


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new order and send a confirmation email to the customer.
        """
        table_id = request.data.get("table_id")
        if not table_id:
            return Response([], status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            date_order = serializer.validated_data["date"]
            table = get_object_or_404(Table, id=table_id)
            if table.orders.filter(date=date_order).exists():
                return Response(
                    {"error": "This table is already booked on this date"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save(table=table)
            headers = self.get_success_headers(serializer.data)
            table_id = serializer.validated_data.get("table_id")
            send_mail(
                "Table order",
                f"Id {table_id}, Date {date_order}",
                HOST_EMAIL,
                [serializer.validated_data.get("customer_email")],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
