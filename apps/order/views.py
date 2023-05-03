from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.order.models import Order, Table
from apps.order.serializer import OrderSerializer, TableSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @action(detail=True, methods=["get"])
    def reservations(self, request, pk=None):
        table = get_object_or_404(Table, pk=pk)
        reserved_dates = table.reservation_set.values_list("reserved_date", flat=True)
        return Response(reserved_dates)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        table_id = request.data.get("table_id")
        table = get_object_or_404(Table, id=table_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(table=table)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=["get"])
    def available_tables(self, request):
        date_str = request.GET.get("date")
        if date_str:
            date = parse_date(date_str)
            reserved_tables = Order.objects.filter(reserved_date=date).values_list("table", flat=True)
            available_tables = Table.objects.exclude(id__in=reserved_tables)
            serializer = TableSerializer(available_tables, many=True)
            return Response(serializer.data)
        else:
            return Response([])
