from rest_framework import routers
from cubeseed.userprofile import views

router = routers.DefaultRouter()

router.register(r'userprofile', views.UserProfileViewSet, basename='userprofile')
router.register(r'userprofilephoto', views.UserProfilePhotoViewSet, basename='userprofilephoto')
