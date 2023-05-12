from django.db import models
from django.utils import timezone
from django.conf import settings


class VitalLog(models.Model):
    WEIGHT = 'weight'
    HEART_RATE = 'heart_rate'
    MOOD = 'mood'
    VITAL_TYPE_CHOICES = [
        (WEIGHT, 'Weight'),
        (HEART_RATE, 'Heart rate'),
        (MOOD, 'Mood'),
    ]
    vital_type = models.CharField(max_length=20, choices=VITAL_TYPE_CHOICES, verbose_name='vital type')
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='value')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='created at')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vital_logs')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user} - {self.vital_type}: {self.value}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.vital_type == VitalLog.WEIGHT:
            self.user.refresh_from_db()
