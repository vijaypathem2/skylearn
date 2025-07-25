from django.urls import path
from . import views

urlpatterns = [
    path('', views.assessment_list, name='assessment_list'),
    path('<int:assessment_id>/', views.take_assessment, name='take_assessment'),
    path('<int:assessment_id>/submit/', views.submit_assessment, name='submit_assessment'),
]