from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin", admin.site.urls),
    # user urls
    path("api/v1/users", include("core.rest.urls.base")),
    # authentication urls
    path("api/v1/auth/", include("authentication.rest.urls.authentications")),
    # profile urls
    path("api/v1/users/profile", include("user_profile.rest.urls.profile")),
    # shop url
    path("api/v1/shops", include("shop.rest.urls.shop")),
    path("api/v1/shops/<str:domain>", include("shop.rest.urls.shop_user")),
    path("api/v1/merchant", include("shop.rest.urls.merchant")),
    # shop product url
    path("api/v1/shops/<str:domain>/products", include("product.rest.urls.product")),
    # customer cart url
    path("api/v1/carts", include("cart.rest.urls.cart")),
    # customer shipping address
    path("api/v1/users/addresses", include("shipping_address.rest.urls.shipping_address")),
    # silk url
    path("silk/", include("silk.urls", namespace="silk")),
    # Spectacular url
    path("", SpectacularSwaggerView.as_view(), name="api-docs"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
