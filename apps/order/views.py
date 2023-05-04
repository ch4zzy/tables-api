from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.order.models import Order, Table
from apps.order.serializer import OrderSerializer, TableSerializer


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
        reserved_dates = Order.objects.filter(table=table).values_list("date", flat=True)
        return Response(reserved_dates)

    @action(detail=False, methods=["get"])
    def available_tables(self, request):
        """
        Return a list of available tables for a specific date.
        """
        date_str = request.GET.get("date")
        if date_str:
            date = parse_date(date_str)
            reserved_tables = Order.objects.filter(date=date).values_list("table", flat=True)
            available_tables = Table.objects.exclude(id__in=reserved_tables)
            serializer = TableSerializer(available_tables, many=True)
            return Response(serializer.data)
        else:
            return Response([])

    @action(detail=False, methods=["get"])
    def occupancy(self, request):
        """
        Return the occupancy percentage for a specific date.
        """
        date_str = request.GET.get("date")
        date = parse_date(date_str)
        reserved_tables = Order.objects.filter(date=date).values_list("table", flat=True)
        total_area = sum([table.width * table.length for table in Table.objects.all()])
        occupied_area = sum(
            [
                order.table.width * order.table.length
                for order in Order.objects.filter(id__in=reserved_tables)
            ]
        )
        occupancy_percentage = round(occupied_area / total_area * 100, 2)
        return Response({"occupancy": occupancy_percentage})


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
        table = get_object_or_404(Table, id=table_id)
        if Order.objects.filter(table=table, date=request.data.get("date")).exists():
            return Response(
                {"error": "This table is already booked on this date"}, status=status.HTTP_400_BAD_REQUEST
            )
        customer_email = request.data.get("customer_email")
        date_order = request.data.get("date")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(table=table)
        headers = self.get_success_headers(serializer.data)
        send_mail(
            "Subject here",
            f"Id {table_id}, Date {date_order}",
            "test@example.com",
            [customer_email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
