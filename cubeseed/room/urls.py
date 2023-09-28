from django.urls import path
from . import views

urlpatterns = [
    path('', views.rooms, name="rooms"),
    path('<slug:slug>/', views.room, name="room"),
]


# from rest_framework import routers
# from cubeseed.room import views

# def register_routes(router):
#     router.register(r"room", views.rooms, basename="room")

#     return router

# urlpatterns = register_routes(routers.DefaultRouter()).urls