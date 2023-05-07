from django.contrib import admin
from habits import models

admin.site.register(models.Habit)
admin.site.register(models.SubscribedHabit)
admin.site.register(models.HabitHistoryLog)
