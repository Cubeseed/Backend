from django.urls import path
from . import views
from .views import MessagesApi
from cubeseed.room import views

urlpatterns = [
    path('', views.rooms, name="rooms"),
    path('<slug:slug>/', views.room, name="room"),
    path('<slug:slug>/messages', MessagesApi.as_view(), name="room"),
    # path('conversations/<name>/', views.ConversationViewSet.as_view({'get': 'retrieve'}), name="conversation"),
]


# from rest_framework import routers
# # from cubeseed.room import views

# def register_routes(router):
#     router.register(r"conversations", views.ConversationViewSet)
#     return router

# urlpatterns = register_routes(routers.DefaultRouter()).urls


