from django.urls import include, path
from rest_framework import routers

from apps.order.views import OrderViewSet, TableViewSet

app_name = "api_order"

router = routers.DefaultRouter()
router.register(r"tables", TableViewSet)
router.register(r"orders", OrderViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
