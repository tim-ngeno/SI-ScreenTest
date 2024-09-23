from django.urls import include, path
from . import views
from .oidc_settings import oidc_callback
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"customers", views.CustomerViewSet, basename="customer")
router.register(r"orders", views.OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
    path("oidc/callback/", oidc_callback, name="oidc_callback"),
]
