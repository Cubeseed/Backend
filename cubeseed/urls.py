"""
URL configuration for cubeseed project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path

from rest_framework import routers, permissions
from rest_framework_nested import routers as drf_nested_routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from cubeseed.userauth.urls import register_routes as register_userauth_routes
from cubeseed.userprofile.urls import register_routes as register_userprofile_routes
from cubeseed.userauth.views import VersionView
from cubeseed.address.views import AddressViewSet
from cubeseed.businessprofile.urls import register_routes as register_businessprofile_routes

from cubeseed.commodity.urls import register_routes as register_commodity_routes
from cubeseed.cluster.urls import register_routes as register_cluster_routes

from cubeseed.farm.views import FarmViewSet, FarmInClusterViewSet

from cubeseed.course.urls import register_routes as register_course_routes
from cubeseed.course_verification.urls import register_routes as register_course_verification_routes

from cubeseed.purchase_orders.urls import register_routes as register_purchase_orders_routes
from cubeseed.farm_planner.urls import register_routes as register_farm_planner_routes

# from cubeseed.room.urls import register_routes as register_conversations_route

# from cubeseed.room.urls import register_routes as register_room_routes
from cubeseed.room import views

from django.conf import settings
from django.conf.urls.static import static


SchemaView = get_schema_view(
    openapi.Info(
        title="Cubeseed API",
        default_version="v1",
        description="This is the RESTful API for the Cubeseed project.",
        terms_of_service="https://www.cubeseed.com/policies/terms/",
        contact=openapi.Contact(email="contact@cubeseed.com"),
        license=openapi.License(name="LGPL License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
register_userauth_routes(router)
register_userprofile_routes(router)
register_businessprofile_routes(router)

register_commodity_routes(router)

register_course_routes(router)
register_course_verification_routes(router)
register_purchase_orders_routes(router)
register_farm_planner_routes(router)


router.register(r"address", AddressViewSet)
register_cluster_routes(router)
router.register(r"farm", FarmViewSet, basename="farm")

# register_conversations_route(router)

# register_room_routes(router)

# Nested Routes for farms in a cluster
# {cluster/{cluster_pk}/farm/}
cluster_router = drf_nested_routers.NestedDefaultRouter(router, r"cluster", lookup="cluster")
cluster_router.register(r"farm", FarmInClusterViewSet, basename="cluster-farm")


urlpatterns = [
    path('chat-media/', include('cubeseed.media_app.urls')),
    path("admin/", admin.site.urls),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", SchemaView.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^swagger/$", SchemaView.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^redoc/$", SchemaView.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/", include(router.urls)),
    path("api/", include(cluster_router.urls)),
    path("api/version", VersionView.as_view()),
    path("api/rooms/", include("cubeseed.room.urls")),
    path("api/conversations", views.ConversationViewSet.as_view({'get': 'list'}), name="conversations"),
]
