from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from instructor.serializer import ExercisesNameSerializer, UserWithoutInstructorSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.models import Instructor, Workout, UserData, WorkOutDate
from user.serializer import UserCardSerializer,  WorkOutsCardSerializer
from django.db.models import Q


def isInstructor(user: User):
    try:
        return Instructor.objects.get(user=user)
    except:
        return False


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_instructor_students(request):
    instructor = isInstructor(request.user)
    if instructor:
        students = instructor.students.all()
        students = UserCardSerializer(students, many=True)
        return Response(students.data)
    else:
        return Response('no instructor found')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_students_without_instructors(request):
    instructor = isInstructor(request.user)
    if instructor:
        user_data_without_instructor = UserData.objects.filter(instructor=None)
        users = []
        for user_data in user_data_without_instructor:
            ins = isInstructor(user_data.user)
            if ins == False:
                users.append(user_data)
        users = UserWithoutInstructorSerializer(users, many=True)
        return Response(users.data)
    else:
        return Response('youre not a instructor')


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def assign_instructor_to_student(request):
    instructor = isInstructor(request.user)
    data = request.data
    if instructor:
        # take the instructor and make him the instructor of the registered user .
        if 'userId' in data:
            user_id = request.data['userId']
            try:
                user = User.objects.get(id=user_id)
            except:
                return Response('invalid user id ')
            else:
                user_data = UserData.objects.get(user=user)
                user_data.instructor = instructor
                user_data.save()
                return Response("instructor assigned to student")
        else:
            return Response('invalid fields ')

    else:
        return Response('youre not a instructor')


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def assign_student_workout(request):
    ins = request.user
    if ins:
        data = request.data
        if 'username' in data and 'workoutId' in data:
            username = data['username']
            workout_id = data['workoutId']
            user = User.objects.get(username=username)
            user_data = UserData.objects.get(user=user)
            workout = Workout.objects.get(id=workout_id)
            workout_date = WorkOutDate.objects.create(workout=workout)
            user_data.pending_workouts.add(workout_date)
            user_data.save()
            return Response('workout assigned')
        # once we have the user id and the workout id we retrive the workout and the user data and then add the workout to the user

    else:
        return Response('youre not a instructor')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_student(request):
    ins = isInstructor(request.user)
    data = request.GET
    if ins:
        # get studnets and remove the specified student
        if 'userId' in data:
            print(ins.students.all())
            try:
                student = ins.students.get(id=data['userId'])
            except:
                return Response('no user found')
            else:
                student.instructor = None
                student.save()
                return Response('deleted successfully')

        else:
            return Response('invalid fields')

    else:
        return Response('youre not a instructor')
