from rest_framework import viewsets, permissions
from .serializers import OrderGetSerializer, OrderPostSerializer
from .models import Order
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status


class OrderList(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderGetSerializer
        return OrderPostSerializer

    serializer_class = get_serializer_class
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = ['selected_products__name',
        'selected_products__brand_name', 'selected_products__material',
        'selected_products__description']
    ordering_fields = '__all__'
    filter_backends = [OrderingFilter, SearchFilter]

    def get_queryset(self):
        if self.request.method == 'GET' and self.request.user.is_admin:
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(customer=user)

    def create(self, request, *args, **kwargs):
        if (request.user.is_superuser):
            return Response({'Message': 'No permissions!'},
            status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_200_OK,
                headers=headers)
