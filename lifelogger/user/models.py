from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser


class ExtendedUser(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False, max_length=255, verbose_name='email')
    habits = models.ManyToManyField('habits.Habit', through='habits.SubscribedHabit')
    allow_email_reminders = models.BooleanField(default=True)

    class Meta:
        ordering = ('date_joined',)

    def send_reminder(self):
        if len(self.habits.all()) > 0:
            habits = '\n'.join([habit.name for habit in self.habits.all()])
            message = f"Howdy, be sure to stop by LifeLogger and update the progress on your habits!" \
                      f"\nHabits:\n" \
                      f"{habits}"
        else:
            message = "You haven't subscribed to any habits yet, head on over to LifeLogger to begin your journey!"

        title = "Don't forget to update your habits!"
        to = [self.email]

        send_mail(
            subject=title,
            message=message,
            from_email="LifeLogger@life.com",
            recipient_list=to,
        )
