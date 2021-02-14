from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate


@api_view(['POST'])
def sign_up(request):
    data = request.data
    # username, email, password, firstname, lastname
    if 'username' in data and 'password' in data and 'email' in data:
        user = authenticate(
            usename=data['username'], password=data['password'])
        if user is not None:
            # some error occured and the user doesnt exist, create a user in that case
            user = User.objects.create_user(
                username=request.data['username'],
                password=request.data['password'],
                email=request.data['email'],
            )
            token = Token.objects.get(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        else:
            # user aldready exists.
            return Response('user_exists', status=status.HTTP_409_CONFLICT)
    else:
        return Response(invalid_fields, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    # sign in
    data = request.data
    if 'username' in data and 'password' in data:
        user = authenticate(
            username=data['username'], password=data["password"])
        if user is not None:
            token = Token.objects.get(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        else:
            # the credentials are invalid.
            return Response('invalid_credentials', status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'error': 'invalid_fields'
        }, status=status.HTTP_401_UNAUTHORIZED)
