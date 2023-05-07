from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path('create', views.UserCreateAPIView.as_view(), name='create-user'),
    path('list', views.UserListAPIView.as_view(), name='list-users'),
    path('<int:pk>', views.UserRetrieveUpdateAPIView.as_view(), name='user'),
    path('update-password', views.PasswordUpdateView.as_view(), name='update-password')
]
