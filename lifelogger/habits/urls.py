from django.urls import path
from habits.views import (
    HabitListCreateAPIView,
    HabitUpdateDetailAPIView,
    SubscribedHabitsListAPIView,
    HabitHistoryLogListAPIView,
    SubscribedHabitsUpdateAPIView,
    AddSubscribedHabitsAPIView
)

app_name = "habits"

urlpatterns = [
    # Implicit "/habits/" in front of each path, from lifelogger.urls
    path('', HabitListCreateAPIView.as_view(), name='habit-list-create'),
    path('<int:pk>', HabitUpdateDetailAPIView.as_view(), name='habit-detail-update'),
    path('subscribed/list', SubscribedHabitsListAPIView.as_view(), name='subscribed-habits-list'),
    path('subscribed/update', SubscribedHabitsUpdateAPIView.as_view(), name='subscribed-habits-update'),
    path('subscribed', AddSubscribedHabitsAPIView.as_view(), name='subscribed-habits'),
    path('history/logs/list', HabitHistoryLogListAPIView.as_view(), name='habit-history-log-list')
]
