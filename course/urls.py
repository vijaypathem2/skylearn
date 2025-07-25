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
    DocumentCreateView, VideoCreateView, ImageCreateView,
)

urlpatterns = [
    path('', Course_Home_ListView.as_view(), name='home'),
    path('courses/create/', CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    # Lessons inside a course
    path('courses/<int:pk>/lessons/', CourseLessonListView.as_view(), name='course_lessons'),
    path('courses/<int:pk>/lessons/add/', LessonCreateView.as_view(), name='lesson_create'),
    path('courses/lessons/<int:pk>/manage/', LessonContentManageView.as_view(), name='lesson_manage'),
    path('courses/lessons/<int:pk>/add-document/', DocumentCreateView.as_view(), name='add_document'),
    path('courses/lessons/<int:pk>/add-video/', VideoCreateView.as_view(), name='add_video'),
    path('courses/lessons/<int:pk>/add-image/', ImageCreateView.as_view(), name='add_image'),

    # Single lesson detail
    path('lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail_view'),

    # Course watch
    path('course/<int:pk>/watch/', CourseDetailWatchView.as_view(), name='course_watch_view'),
]









# from django.urls import path
# from .views import (
#     Course_Home_ListView,
#     CourseDetailView,
#     CourseCreateView,
#     CourseUpdateView,
#     CourseDeleteView,
#     CourseLessonView,
#     CourseDetailWatchView,
#     LessonView,
#     CourseLessonListView, LessonCreateView, LessonDetailView,
# )

# urlpatterns = [
#     path('', Course_Home_ListView.as_view(), name='home'),
#     path('courses/create/', CourseCreateView.as_view(), name='course_create'),
#     path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
#     path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
#     path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
#     path('courses/<int:pk>/lessons/', CourseLessonView.as_view(), name='course_lessons'),
#     path('course/<int:pk>/',CourseDetailWatchView.as_view(),name = 'course_watch_view'),
#     path('lesson/<int:pk>/',LessonView.as_view(),name = 'lesson_detail_view'),
#     path('courses/<int:pk>/lessons/', CourseLessonListView.as_view(), name='course_lessons'),
#     path('courses/<int:pk>/lessons/add/', LessonCreateView.as_view(), name='lesson_create'),
#     path('lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
# ]