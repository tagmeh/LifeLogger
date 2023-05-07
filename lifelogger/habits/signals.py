from django.db.models.signals import post_save
from django.dispatch import receiver

from habits.models import SubscribedHabit, HabitHistoryLog


@receiver(post_save, sender=SubscribedHabit)
def create_habit_history_log(sender, instance, **kwargs):
    """
    This function is a signal handler that is triggered when the updated_today
    field of a SubscribedHabit instance is changed to True. It creates a new
    HabitHistoryLog object and saves it to the database with the user and habit
    information, as well as storing if the user felt they achieved their daily goal/habit.
    """

    achieved = kwargs.get('achieved')  # Did the user feel like they achieved or accomplished their goal/habit today?
    print(f"{sender=}")
    print(f"{instance=}")
    print(f"{kwargs=}")

    # if instance.updated_today:
    #     HabitHistoryLog.objects.create(
    #         user=instance.user,
    #         habit=instance.habit,
    #         achieved=achieved
    #     )
