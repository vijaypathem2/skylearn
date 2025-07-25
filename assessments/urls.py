from .views import AssessmentListView, AssessmentDetailView, AssessmentCreateView, AssessmentUpdateView,  AssessmentDeleteView, QuestionListView, QuestionCreateView
from django.urls import path
from . import views

urlpatterns = [
    path("", AssessmentListView.as_view(), name="assessment_list"),  
    path("assessmentview/<int:pk>/", AssessmentDetailView.as_view(), name="assessment_detail"),
    path("assessment/create/", AssessmentCreateView.as_view(), name="assessment_create"),
    path('assessment/<int:pk>/edit/', AssessmentUpdateView.as_view(), name='assessment_update'),
    path('assessment/<int:pk>/delete/', AssessmentDeleteView.as_view(), name='assessment_delete'),
    path('questions/', QuestionListView.as_view(), name='question_list'),
    path("assessment/<int:assessment_id>/question/create/", QuestionCreateView.as_view(), name="question_create"),
    
    
]
