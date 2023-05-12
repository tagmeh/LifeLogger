from django.urls import path
from habits import views

app_name = "habits"

urlpatterns = [
    path('habits/', views.HabitListCreateAPIView.as_view(), name='habit-list-create'),
    path('habits/<int:pk>', views.HabitUpdateDetailAPIView.as_view(), name='habit-detail-update'),
    path('habits/subscribed/list', views.SubscribedHabitsListAPIView.as_view(), name='subscribed-habits-list'),
    path('habits/subscribed/update', views.SubscribedHabitsUpdateAPIView.as_view(), name='subscribed-habits-update'),
    path('habits/subscribed', views.AddSubscribedHabitsAPIView.as_view(), name='subscribed-habits'),
    path('habits/history/logs/list', views.HabitHistoryLogListAPIView.as_view(), name='habit-history-log-list'),
]
