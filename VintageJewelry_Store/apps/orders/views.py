from rest_framework import viewsets, permissions
from .serializers import OrderGetSerializer, OrderPostSerializer
from .models import Order
from rest_framework.filters import SearchFilter


class OrderViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderGetSerializer
        return OrderPostSerializer

    serializer_class = get_serializer_class
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = ['selected_products__name',
        'selected_products__brand_name', 'selected_products__material',
        'selected_products__description']
    filter_backends = [SearchFilter]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(customer=user)
