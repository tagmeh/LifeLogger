from django.urls import path
from main import views

urlpatterns = [
    path('account/create', views.UserCreateAPIView.as_view(), name='create-account'),
    path('account/list', views.UserListAPIView.as_view(), name='list-account'),
    path('account/<int:pk>', views.UserRetrieveUpdateAPIView.as_view(), name='account'),
]
