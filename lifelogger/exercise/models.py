# from django.contrib.auth import get_user_model
# from django.db import models
#
# User = get_user_model()
#
#
# class Exercise(models.Model):
#     """
#     Base Exercise class
#     """
#     name = models.CharField(max_length=150)
#     description = models.TextField()
#     video_link = models.TextField()
#     timestamp = models.DateTimeField(auto_created=True)
#     instructions = models.TextField()
#
#
# class WeightTrainingExercise(models.Model):
#     """
#     Exercises that are best described with weights, repetition, and sets.
#     These might include:
#         - weight lifting
#         - resistance training
#         - body weight exercises
#         - calisthenics
#     """
#     exercise = models.OneToOneField(Exercise, on_delete=models.CASCADE)
#     weight = models.PositiveIntegerField()
#     reps = models.PositiveIntegerField()
#     sets = models.PositiveIntegerField()
#
#
# class FlexibiltyExercise(models.Model):
#     """
#     Exercises that are best described with repetition.
#     These might include:
#         - stretches
#     """
#     exercise = models.OneToOneField(Exercise, on_delete=models.CASCADE)
#     reps = models.PositiveIntegerField()
#
#
# class CardioExercise(models.Model):
#     """
#     Exercises are best described with distance and duration.
#     """
#     exercise = models.OneToOneField(Exercise, on_delete=models.CASCADE)
#     distance = models.PositiveIntegerField()
#     duration = models.PositiveIntegerField()
#
#
# class HealthStats(models.Model):
#     """
#     A model of snapshot user data.
#     """
#     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     heartrate = models.PositiveIntegerField()
#     weight = models.PositiveIntegerField()
#     mood = models.CharField(max_length=100)
#
#     def __str__(self):
#         return f'HealthStats for {self.user.username}'
