from rest_framework import serializers
from .models import Workout, UserData, Exercise, WorkOutDate, Post


def getTotalTime(rest_time, active_time, num_exercises):
    return active_time * num_exercises + rest_time * (num_exercises - 1)


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"


class WorkOutsCardSerializer(serializers.ModelSerializer):
    # exercise = ExerciseSerializer(many=True)
    details = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ["details"]

    def get_details(self, obj):
        muscle = []
        for i in obj.exercise.all():
            if i.muscle in muscle:
                continue
            else:
                muscle.append(i.muscle)
        total_time = getTotalTime(
            obj.rest_time, obj.exercise_time, len(obj.exercise.all()))
        return {
            'totalTime': total_time,
            'name': obj.name,
            'muscles': muscle,
            'id': obj.id
        }

# time, body types, name , date


class WorkOutDateCardSerializer(serializers.ModelSerializer):
    workout = WorkOutsCardSerializer()

    class Meta:
        model = WorkOutDate
        fields = ("__all__")


class UserCardSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = UserData
        fields = ('username', 'status', 'id')


class UserSearchSerializer(serializers.ModelSerializer):
    # there are 3 different possibilites , requested, follwing and follow back
    # level of priority
    # requested , the user has a pending follow request,
    # following :  obvio
    username = serializers.SerializerMethodField()
    btn_action = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    def get_btn_action(self, obj):
        logged_in_user = self.context['user']
        user = obj  # this is the other users data
        btn_action = 'follow'  # default
        if logged_in_user in user.requests.all():
            btn_action = 'requested'
        elif logged_in_user in user.followers.all():
            btn_action = 'following'
        return btn_action

    def get_id(self, obj):
        print('from user search serializer ')
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = UserData
        fields = ('username', 'status', 'id', 'btn_action')


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Post
        fields = ("id", "caption", "date", "user")


class UserProfileSerializerInitialLoad(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_posts(self, obj):
        user = obj.user
        user.post_set.all()
        posts = PostSerializer(user.post_set.all(), many=True)
        return posts.data

    def get_followers(self, obj):
        return len(obj.followers.all())

    def get_following(self, obj):
        return len(obj.user.following.all())

    class Meta:
        model = UserData
        fields = ('id', 'user', 'status', 'posts', 'followers',
                  'following', 'instructor')
