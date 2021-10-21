from django.urls import include, path
from rest_framework import routers
from .views import ProductList, AdminProductsList

router = routers.DefaultRouter()
router.register(r'products', ProductList)
router.register(r'refresh_products', AdminProductsList,
basename='refresh_products')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
    namespace='rest_framework'))
]
