from django.urls import path
from habits.views import HabitListAPIView, HabitDetailAPIView, UserHabitsDetailAPIView, UserHabitsListCreateAPIView

urlpatterns = [
    path('habits/', HabitListAPIView.as_view(), name='habit-list'),
    path('habits/<int:pk>/', HabitDetailAPIView.as_view(), name='habit-detail'),
    path('user-habits/', UserHabitsListCreateAPIView.as_view(), name='user-habit-list'),
    path('user-habits/<int:pk>/', UserHabitsDetailAPIView.as_view(), name='user-habit-detail'),
]