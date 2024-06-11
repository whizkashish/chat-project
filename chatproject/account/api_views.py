from rest_framework import generics, permissions, authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, CurrentUserSerializer

class UserCreateView(generics.CreateAPIView):
    """View for Register."""
    serializer_class = UserSerializer

class CurrentUserDetailView(generics.RetrieveAPIView):
    serializer_class = CurrentUserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
