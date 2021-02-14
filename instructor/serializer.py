from rest_framework import serializers
from .models import Instructor
from user.models import UserData, Exercise, Workout
from user.serializer import getTotalTime


class ExercisesNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ("name", "id", "muscle")


class UserWithoutInstructorSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(request, obj):
        return obj.user.username

    class Meta:
        model = UserData
        fields = ("id", "username", "status")


class WorkoutSerializer(serializers.ModelSerializer):
    total_time = serializers.SerializerMethodField()
    exercise = ExercisesNameSerializer(many=True)

    class Meta:
        model = Workout
        fields = "__all__"

    def get_total_time(self, obj):
        return getTotalTime(obj.rest_time, obj.exercise_time, len(obj.exercise.all()))
