from rest_framework import generics, permissions, authentication
from .serializers import UserSerializer, CurrentUserSerializer
from django.contrib.auth.models import User
class UserCreateView(generics.CreateAPIView):
    """View for Register."""
    serializer_class = UserSerializer

class CurrentUserDetailView(generics.RetrieveAPIView):
    serializer_class = CurrentUserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserList(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_objects(self):
        return User.objects.exclude(id=self.user.id).exclude(is_superuser=True, is_staff=True)