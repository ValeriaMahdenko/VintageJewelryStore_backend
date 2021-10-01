from django.urls import include, path
from rest_framework import routers
from .views import ProductList, MyProductsList

router = routers.DefaultRouter()
router.register(r'products', ProductList)
router.register(r'my_products', MyProductsList, basename='my_products')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
    namespace='rest_framework'))
]
