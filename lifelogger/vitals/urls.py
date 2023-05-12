from django.urls import path
from user import views

app_name = "vitals"

urlpatterns = [
    path('create', views.UserCreateAPIView.as_view(), name='create-user'),
    path('list', views.UserListAPIView.as_view(), name='list-users'),
    path('<int:pk>', views.UserRetrieveUpdateAPIView.as_view(), name='user'),
]
