from django.contrib.auth import get_user_model
from django.db import models


class Habit(models.Model):
    name = models.CharField(max_length=50)
    is_good_habit = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} Type: {'Good' if self.is_good_habit else 'Bad'}"


class UserHabits(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateField()
    habits = models.ManyToManyField(Habit, blank=True)

    def __str__(self):
        return f"{self.user.username} on {self.date}"

