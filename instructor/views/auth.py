from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from instructor.models import Instructor
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def get_token(request):
    # sign in
    data = request.data
    if 'username' in data and 'password' in data:
        user = authenticate(
            username=data['username'], password=data["password"])
        if user is None:
            return Response('invalid_credentials', status=status.HTTP_400_BAD_REQUEST)
        try:
            instructor = Instructor.objects.get(user=user)
        except:
            return Response('no user found')
        else:
            token = Token.objects.get(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)

    else:
        return Response({
            'error': 'invalid_fields'
        }, status=status.HTTP_400_BAD_REQUEST)
