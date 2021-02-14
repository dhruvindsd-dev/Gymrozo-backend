from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from instructor.models import Instructor
statusChoices = (
    ('Newbie', 'Newbie'),
    ('Intermediate', 'Intermediate'),
    ('Ace', 'Ace'),
    ('The Rock', 'The Rock'),
)


@receiver(post_save, sender=User)
def createUserData(sender, instance=None, created=False, **kwargs):
    if created:
        # whenever a new user is created we create a token for auth and userData
        Token.objects.create(user=instance)
        UserData.objects.create(user=instance)


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # show follow
    requests = models.ManyToManyField(
        User, null=True, blank=True, related_name='requests_made')
    followers = models.ManyToManyField(
        User, null=True, blank=True, related_name='following')
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE,  null=True, blank=True, related_name='students')
    status = models.CharField(
        max_length=20, choices=statusChoices, default='Newbie')
    dateJoined = models.DateField(auto_now_add=True)
    pending_workouts = models.ManyToManyField(
        "WorkOutDate", related_name='pending', null=True, blank=True)
    completed_workouts = models.ManyToManyField(
        "WorkOutDate", related_name='completed_workouts', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}({self.user.id})"

# user post


class Post(models.Model):
    # img , caption, date
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Exercise(models.Model):
    # type, gif,targettedbodypart, name, description(optional)
    # type = models.CharField(max_length=50) # endurance, strength, balance,
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, null=True)
    # chest, back, traps, shoulders, triceps, biceps, forearms.| calves, hips,| abs, obliques
    muscle = models.CharField(max_length=50)


class Workout(models.Model):
    name = models.CharField(max_length=50)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, null=True, blank=True)
    exercise = models.ManyToManyField(Exercise)
    # rest_time and exercise time in seconds
    rest_time = models.IntegerField(default=30)
    exercise_time = models.IntegerField(default=30)


class WorkOutDate(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
