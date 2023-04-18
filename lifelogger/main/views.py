from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView

from .serializers import UserSerializer

User = get_user_model()


class UserAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

