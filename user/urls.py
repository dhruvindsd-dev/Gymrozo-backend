from django.urls import path
from .views.auth import *
from .views.user import *

urlpatterns = [
    path('sign-up', sign_up),
    path('get-token', get_token),
    path('get-user-workouts/<str:type>', get_user_workouts),
    path('create-user-post', new_post),
    path('search-user', search_user),
    path('user-social-actions/<str:action_type>', user_social_actions),
    path('get-user-feed', get_user_feed),
    path('get-user-profile-initial-load', get_user_profile_initial_load),
    path('workout-complete', workout_complete),

    path('test', testing)
]
