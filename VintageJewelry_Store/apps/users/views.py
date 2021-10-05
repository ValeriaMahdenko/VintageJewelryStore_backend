from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializers import (
    UserSerializer, SuperUserSerializer)
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .forms import ShopUserForm
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

User = get_user_model()


def indexView(request):
    user = request.user
    form = ShopUserForm()
    users = User.objects.filter(pk=user.pk)
    return render(request, "index.html", {"form": form, "users": users})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        form = ShopUserForm()
        users = User.objects.filter(pk=user.pk)
        return render(self.request, "index.html", {"form": form, "users": users})

    def create(self, request):
        if request.is_ajax and request.method == "POST":
            # get the form data
            form = ShopUserForm(request.POST)
            # save the data and after fetch the object in instance
            if form.is_valid():
                #form.save()
                # serialize in new participant object in json
                # send to client side.
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return JsonResponse({"instance": serializer.data}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)


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
