"""Room Urls"""
from django.urls import path
from . import views
from .views import MessagesApi, UploadEndpoint, RefreshURLView, CheckURLView
from cubeseed.room import views

urlpatterns = [
    path('upload', UploadEndpoint.as_view(), name="uploads"),
    path('refresh-url/', RefreshURLView.as_view(), name="refresh-url"),
    path('check-url/', CheckURLView.as_view(), name="check-url"),
    path('<slug:slug>/messages', MessagesApi.as_view(), name="room"),
]



