from .views import AssessmentListView, AssessmentDetailView, AssessmentCreateView, AssessmentUpdateView,  AssessmentDeleteView
from django.urls import path

urlpatterns = [
    path("", AssessmentListView.as_view(), name="assessment_list"),  
    path("assessmentview/<int:pk>/", AssessmentDetailView.as_view(), name="assessment_detail"),
    path("assessment/create/", AssessmentCreateView.as_view(), name="assessment_create"),
    path('assessment/<int:pk>/edit/', AssessmentUpdateView.as_view(), name='assessment_update'),
    path('assessment/<int:pk>/delete/', AssessmentDeleteView.as_view(), name='assessment_delete'),
]
