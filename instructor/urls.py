from django.urls import path
from instructor.views.auth import get_token
from instructor.views.students import *
from instructor.views.workouts import *
urlpatterns = [
    path('get-instructor-token', get_token),
    path('get-instructor-students', get_instructor_students),
    path('get-all-exercises-name', get_all_exercises_name),
    path('get-instructor-workouts', get_instructor_workouts),
    path('create-instructor-workout', new_instructor_workout),
    path('get-students-without-instructors', get_students_without_instructors),
    path('assign-instructor-to-student', assign_instructor_to_student),
    path('assign-student-workout', assign_student_workout),
    path('get-workout-from-id', get_workout_from_id),
    path('remove-student', remove_student),


]
