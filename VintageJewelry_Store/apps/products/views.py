from rest_framework import viewsets, status
from .serializers import ProductGetSerializer, ProductSerializer
from .models import Product
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response


class ProductList(viewsets.ReadOnlyModelViewSet):
    search_fields = ['name', 'brand_name', 'material', 'description']
    ordering_fields = '__all__'
    filter_backends = [OrderingFilter, SearchFilter]

    queryset = Product.objects.all()
    serializer_class = ProductGetSerializer


class MyProductsList(viewsets.ModelViewSet):
    search_fields = ['name', 'brand_name', 'material', 'description']
    ordering_fields = '__all__'
    filter_backends = [OrderingFilter, SearchFilter]
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

    def get_queryset(self):
        return Product.objects.filter(owner_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)
