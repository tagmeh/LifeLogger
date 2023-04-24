from django.urls import path
from habits.views import HabitList, HabitDetail, UserHabitsDetail, UserHabitsList

urlpatterns = [
    path('habits/', HabitList.as_view(), name='habit-list'),
    path('habits/<int:pk>/', HabitDetail.as_view(), name='habit-detail'),
    path('user-habits/', UserHabitsList.as_view(), name='user-habit-list'),
    path('user-habits/<int:pk>/', UserHabitsDetail.as_view(), name='user-habit-detail'),
]