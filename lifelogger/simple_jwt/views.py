from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

@extend_schema(tags=['Authentication'])
class CustomTokenObtainPairView(TokenObtainPairView):

    @extend_schema(
        summary='Generates the initial access and refresh tokens',
        operation_id='auth-token-create'
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['Authentication'])
class CustomTokenRefreshView(TokenRefreshView):

    @extend_schema(
        summary='Refreshes your access and refresh tokens',
        operation_id='auth-token-refresh'
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)