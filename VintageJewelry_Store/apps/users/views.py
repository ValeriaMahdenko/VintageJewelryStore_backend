from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializers import (
    UserSerializer, SuperUserSerializer)
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.pk)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SuperUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_admin=True)
    serializer_class = SuperUserSerializer
    permission_classes = [IsAdminUser]
