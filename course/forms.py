from django import forms
from accounts.models import User
from course.models import Upload
from course.models import UploadVideo
from course.models import Course
from .models import Lesson
from .models import Document, Video, Image

class UploadFormVideo(forms.ModelForm):
    class Meta:
        model = UploadVideo
        fields = ['title', 'video']


class UploadFormFile(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['title', 'file']  # adjust fields as per your Upload model

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            "title", "description", "content", "lesson_type",
            "duration_minutes", "sort_order", "is_preview", "is_mandatory"
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'short_description',
            'thumbnail',
            'banner_image',
            'department',
            'level',
            'learning_outcomes',
            'status'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'learning_outcomes': forms.Textarea(attrs={'rows': 3}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file', 'description', 'source_links', 'is_downloadable']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file', 'video_link', 'description']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image_file', 'image_link', 'description']


