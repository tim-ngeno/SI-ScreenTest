from django.urls import include, path
from . import views
from .oidc_settings import oidc_callback
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"customers", views.CustomerViewSet)
router.register(r"orders", views.OrderViewSet)

urlpatterns = [
    # path("", views.get_customers, name="customers"),
    path("", include(router.urls)),
    # path("orders/", views.get_orders, name="orders"),
    path("oidc/callback/", oidc_callback, name="oidc_callback"),
]
