from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path('main/create', views.UserCreateAPIView.as_view(), name='create-user'),
    path('main/list', views.UserListAPIView.as_view(), name='list-users'),
    path('main/<int:pk>', views.UserRetrieveUpdateAPIView.as_view(), name='user'),
    path('main/update-password', views.PasswordUpdateView.as_view(), name='update-password'),
]
