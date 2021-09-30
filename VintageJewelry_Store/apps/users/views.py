from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializers import (
    UserSerializer, SuperUserSerializer)
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateDestroyAPIView

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


class RetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.pk)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        queryset = User.objects.filter(pk=request.user.pk)
        queryset.delete()
        return Response({'Message': 'Success!'}, status=status.HTTP_200_OK)


class SuperUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_admin=True)
    serializer_class = SuperUserSerializer
    permission_classes = [IsAdminUser]
