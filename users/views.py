from rest_framework import viewsets, mixins, permissions
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegisterSerializer, UserDetailSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

User = get_user_model()

class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
