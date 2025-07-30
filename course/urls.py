from django.urls import path
from .views import (
    Course_Home_ListView,
    CourseDetailView,
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView,
    CourseLessonListView,
    CourseDetailWatchView,
    LessonCreateView,
    LessonDetailView,
    LessonContentManageView,
    DocumentCreateView, 
    VideoCreateView, 
    ImageCreateView,
    LessonStartView,
    LessonFinishView,
    AssignCourseView,
    SelfEnrollCourseView,
    MyCoursesView
)

urlpatterns = [
    path('', Course_Home_ListView.as_view(), name='home'),  # home page

    # Lessons inside a course — keep these ABOVE course_detail to avoid conflicts
    path('courses/<int:pk>/lessons/', CourseLessonListView.as_view(), name='course_lessons'),
    path('courses/<int:pk>/lessons/add/', LessonCreateView.as_view(), name='lesson_create'),
    path('courses/lessons/<int:pk>/manage/', LessonContentManageView.as_view(), name='lesson_manage'),
    path('courses/lessons/<int:pk>/add-document/', DocumentCreateView.as_view(), name='add_document'),
    path('courses/lessons/<int:pk>/add-video/', VideoCreateView.as_view(), name='add_video'),
    path('courses/lessons/<int:pk>/add-image/', ImageCreateView.as_view(), name='add_image'),

    # Lesson detail & start/finish
    path('lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail_view'),
    path('lesson/<int:pk>/start/', LessonStartView.as_view(), name='lesson_start'),
    path('lesson/<int:pk>/finish/', LessonFinishView.as_view(), name='lesson_finish'),

    # Course creation & management
    path('courses/create/', CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    # Course detail — must be AFTER lessons URLs
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),

    # Course watch view
    path('course/<int:pk>/watch/', CourseDetailWatchView.as_view(), name='course_watch_view'),

    # Assign & enroll
    path('course/<int:pk>/assign/', AssignCourseView.as_view(), name='assign_course'),
    path('course/<int:pk>/self-enroll/', SelfEnrollCourseView.as_view(), name='self_enroll'),

    # My courses
    path('my-courses/', MyCoursesView.as_view(), name='my_courses'),
]
