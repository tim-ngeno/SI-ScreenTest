from django.contrib import admin
from django.urls import include, path
from mozilla_django_oidc.views import OIDCAuthenticationRequestView
from mozilla_django_oidc.views import OIDCAuthenticationCallbackView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path(
        "oidc/authenticate/",
        OIDCAuthenticationRequestView.as_view(),
        name="oidc_login",
    ),
    path(
        "oidc/callback/", OIDCAuthenticationCallbackView.as_view(), name="oidc_callback"
    ),
    path("", include("api.urls")),
]
