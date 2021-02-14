from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.models import Exercise
from instructor.serializer import ExercisesNameSerializer, WorkoutSerializer
from user.serializer import WorkOutsCardSerializer
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.models import User
from user.models import Instructor, Workout
from django.db.models import Q


def is_instructor(user):
    try:
        return Instructor.objects.get(user=user)
    except:
        return False


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_exercises_name(request):
    # name and if for the workout creation
    exercises = Exercise.objects.all().order_by('muscle')
    exercises = ExercisesNameSerializer(exercises, many=True)
    return Response(exercises.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_instructor_workout(request):
    data = request.data
    instructor = is_instructor(request.user)
    if instructor:
        workout = Workout.objects.create(
            name=data['name'],
            instructor=instructor,
            rest_time=data['restTime'], exercise_time=data['activeTime'])
        exercise_ids = data['exercises'].split(',')
        for i in exercise_ids:
            exercise = Exercise.objects.get(id=i)
            workout.exercise.add(exercise)
        workout.save()
        return Response('workout created')
    else:
        return Response('youre not a instructor')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_instructor_workouts(request):
    instructor = is_instructor(request.user)
    if instructor:
        workouts = Workout.objects.filter(
            Q(instructor=instructor) | Q(instructor=None))
        workouts = WorkOutsCardSerializer(workouts, many=True)
        return Response(workouts.data)
    else:
        return Response("No Instructor Found")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_workout_from_id(request):
    data = request.GET
    if 'workoutId' in data:
        workout = Workout.objects.get(id=data['workoutId'])
        workout = WorkoutSerializer(workout)
        return Response(workout.data)

    else:
        return Response('invalid fields')
