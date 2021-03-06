from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from django_email_verification import urls as email_urls


router = routers.DefaultRouter()
router.register(r'superusers', views.SuperUserViewSet)

urlpatterns = [
    path('users/', views.RetrieveUpdateDestroyAPIView.as_view(),
        name='read_update_delete'),
    path('users/register/', views.UserViewSet.as_view({'post': 'create'}),
        name='register'),
    path('users/login/', TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(),
        name='token_refresh'),
    path('users/email-confirm/', include(email_urls)),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
        namespace='rest_framework'))
]
