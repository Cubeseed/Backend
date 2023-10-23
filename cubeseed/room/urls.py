from django.urls import path
from . import views
from .views import MessagesApi
from cubeseed.room import views

urlpatterns = [
    path('', views.rooms, name="rooms"),
    path('<slug:slug>/', views.room, name="room"),
    path('<slug:slug>/messages', MessagesApi.as_view(), name="room"),
]



