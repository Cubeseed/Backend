from rest_framework import routers
from cubeseed.userprofile import views

router = routers.DefaultRouter()

router.register(r'userprofile', views.UserProfileViewSet)
router.register(r'userprofilephoto', views.UserProfilePhotoViewSet)

urlpatterns = router.urls
