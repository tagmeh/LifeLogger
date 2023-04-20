from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListCreateAPIView

from .serializers import UserSerializer

User = get_user_model()


@extend_schema(
    parameters=[
        UserSerializer,
        OpenApiParameter(
            name='password',
            type=OpenApiTypes.PASSWORD
        )
    ]
)
class UserAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
