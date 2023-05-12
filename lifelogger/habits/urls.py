from django.urls import path
from habits import views

app_name = "habits"

urlpatterns = [
    path('', views.HabitListCreateAPIView.as_view(), name='habit-list-create'),
    path('<int:pk>', views.HabitUpdateDetailAPIView.as_view(), name='habit-detail-update'),
    path('subscribed/list', views.SubscribedHabitsListAPIView.as_view(), name='subscribed-habits-list'),
    path('subscribed/update', views.SubscribedHabitsUpdateAPIView.as_view(), name='subscribed-habits-update'),
    path('subscribe', views.SubscribeHabitsAPIView.as_view(), name='subscribe-habits'),
    path('unsubscribe', views.UnsubscribeHabitsAPIView.as_view(), name='unsubscribe-habits'),
    path('history/logs/list', views.HabitHistoryLogListAPIView.as_view(), name='habit-history-log-list'),
]
