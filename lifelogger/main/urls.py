from django.urls import path
from main import views

urlpatterns = [
    path('account/', views.UserListCreateAPIView.as_view(), name='account')
    # other URL patterns
]
