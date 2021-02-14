from django.contrib.auth.models import User
from .models import Exercise, Workout, UserData
# from .serializer import WorkOutsSerializer
# Create your tests here.


def add_users(num):
    for i in range(num):
        User.objects.create_user(
            username=f"pickle{i}", password="pickle", email=f"dummyemail@something.com{i}")


def add_exercise(num):
    for i in range(num):
        Exercise.objects.create(
            name=f"test exercise {i}", description=f"test exercise", muscle="full body")


def serializerTest():
    user = User.objects.get(id=2)
    userd = UserData.objects.get(user=user)
    print(userd)
    pw = userd.pending_workouts.all()
    # ws = WorkOutsSerializer(pw, many=True)
    # return ws.data
