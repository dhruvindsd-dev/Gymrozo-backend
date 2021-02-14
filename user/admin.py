from django.contrib import admin
from .models import UserData, Exercise, Workout, WorkOutDate, Post
# Register your models here.
admin.site.register(UserData)
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(Post)

# remove
admin.site.register(WorkOutDate)
