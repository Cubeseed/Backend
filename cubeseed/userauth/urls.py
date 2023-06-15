from cubeseed.userauth import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'register', views.RegisterUserView, basename='register')
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = router.urls