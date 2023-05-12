from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models


class Habit(models.Model):
    """
    A Habit represents a goal or habit a user wants to work towards.
    A user can make progress against being successful with the Habit on a daily basis.
    Examples of Habits could be "Avoid Soda" or "Go on a walk".
    """

    # Name of the habit. The way it's phrased will help indicate if it's a "good" or "bad" habit.
    name = models.CharField(max_length=50, validators=[validators.MinLengthValidator(5)])
    # Is this a good habit they are working towards, or a bad habit they're trying to avoid.
    is_good_habit = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Updates on creation only.

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name} Type: {'Good' if self.is_good_habit else 'Bad'}"


class SubscribedHabit(models.Model):
    """
    This model stores the relationship between a User and a Habit they've chosen to work towards.
    We log when they subscribed to it, for future display settings.
    We also show if they've reviewed and updated the Habit today, which is reset at midnight each night.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    updated_today = models.BooleanField(default=False)  # Whether the user has reviewed and updated their habit today.
    subscribed_on = models.DateTimeField(auto_now_add=True)  # Updates on creation only.

    def __str__(self):
        return f"User {self.user.email} subscribed to Habit '{self.habit.name}' on {self.subscribed_on}"

    def log_progress(self, achieved: bool):
        """
        Logs the user's progress on the subscribed habit.
        Creates a new HabitHistoryLog instance for the current user and habit.
        """
        HabitHistoryLog.objects.create(user=self.user, habit=self.habit, achieved=achieved)
        self.updated_today = True
        self.save()


class HabitHistoryLog(models.Model):
    """
    This is a log of when a user updates one of the habits they are subscribed to.
    This retains a history of whether the user feels they've achieved their daily goal,
      or preformed the habit they subscribed to.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)  # Updates on creation only.
    achieved = models.BooleanField()  # Did the user feel like they achieved their daily goal/habit.

    def __str__(self):
        return f"User {self.user.email} achieved Habit {self.habit.name} on {self.created_on}: {self.achieved}"
