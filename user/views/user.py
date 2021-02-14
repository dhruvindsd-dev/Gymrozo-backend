from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from django.shortcuts import render
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.dummyaCreations import *
from user.models import Post, UserData, Post, WorkOutDate
from user.serializer import WorkOutDateCardSerializer, UserSearchSerializer, PostSerializer, UserProfileSerializerInitialLoad


# get workouts:
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_workouts(request, type):
    workouts = UserData.objects.get(
        user=request.user)
    if type == 'pending':
        workouts = workouts.pending_workouts.all()
    elif type == 'past':
        workouts = workouts.completed_workouts.all()
    else:
        return Response('invalid type', status=status.HTTP_400_BAD_REQUEST)
    workouts = WorkOutDateCardSerializer(workouts.order_by('date'), many=True)
    return Response(workouts.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_post(request):
    data = request.data
    if 'caption' in data:
        post = Post.objects.create(user=request.user, caption=data['caption'])
        return Response('post created')
    else:
        return Response('invalid fields')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_user(request):

    data = request.GET
    user = request.user
    if 'query' in data:
        users = UserData.objects.filter(
            user__username__contains=data['query']).exclude(user=user)
        users = UserSearchSerializer(
            users, many=True, context={'user': user})
        return Response(users.data)
    else:
        return Response('invalid fields')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile_initial_load(request):
    # get user if and send all the detaisl
    data = request.GET
    if 'username' in data:
        try:
            user = User.objects.get(username=data['username'])
        except:
            return Response('no user found')
        else:
            user_data = UserData.objects.get(user=user)
            user_data = UserProfileSerializerInitialLoad(user_data)
            print(user_data.data)
            return Response(user_data.data)
    else:
        return Response('invalid fields')


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# follow, unfollow, request functionality
def user_social_actions(request, action_type):
    # get the user making the request
    # get the user id the user wants to follow and add the current user to his requests list .
    data = request.data
    logged_in_user = request.user  # the user whos actually doing the action
    if 'userToRequestId' in data:
        try:
            user = User.objects.get(id=data['userToRequestId'])
        except:
            return Response('invalid user id ')
        else:
            # follow, unfollow, undorequest
            user_data = UserData.objects.get(user=user)
            if action_type == 'follow':
                user_data.requests.add(logged_in_user)
            elif action_type == 'unfollow':
                user_data.followers.remove(logged_in_user)
            elif action_type == 'removeFollowRequest':
                user_data.requests.remove(logged_in_user)
            else:
                return Response('invalid action type')

            return Response('action done')

    else:
        return Response('invalid fields ')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_feed(request):
    # get the user data , then get all the followers
    user = UserData.objects.get(user=request.user).user
    # getting all the users who have this user in the their followers list
    followers = user.following.all()
    print(followers)
    if len(followers) == 0:
        return Response('no_followers')
    query = Q(user=followers[0].user)
    for user_data in followers[1:]:
        query = query | Q(user=user_data.user)
    posts = Post.objects.filter(query).order_by('-id')
    print(posts)
    posts = PostSerializer(posts, many=True)
    return Response(posts.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def workout_complete(request):
    user = request.user
    data = request.GET
    if 'workoutDateId' in data:
        # check if the workout is there in the pending workouts,
        try:
            workout = WorkOutDate.objects.get(id=int(data['workoutDateId']))
        except:
            return Response('no workout found')
        else:
            user_data = UserData.objects.get(user=user)
            try:
                pending_workout = user_data.pending_workouts.get(
                    id=data['workoutDateId'])
            except:
                return Response('pending workout not found ')
            else:
                user_data.pending_workouts.remove(pending_workout)
                user_data.completed_workouts.add(pending_workout)
                return Response('pending workout added to completed workout successful')

    else:
        return Response('invalid fields')


@api_view(['GET'])
def testing(request):
    # datas = serializerTest()
    # add_users(10)
    # add_exercise(10)
    return Response({'testing': 'testing'})
