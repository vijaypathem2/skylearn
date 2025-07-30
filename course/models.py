from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# -----------------
# Department
# -----------------
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    head_of_department = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# -----------------
# Course
# -----------------
class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=500, blank=True, null=True)
    thumbnail = models.CharField(max_length=255, blank=True, null=True)
    banner_image = models.ImageField(upload_to='course_banner_images/', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    learning_outcomes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# -----------------
# Lesson
# -----------------
class Lesson(models.Model):
    LESSON_TYPE_CHOICES = [
        ('video', 'Video'),
        ('document', 'Document'),
        ('image', 'Image'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES)
    duration_minutes = models.IntegerField(null=True, blank=True)
    sort_order = models.IntegerField()
    is_preview = models.BooleanField(default=False)
    is_mandatory = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# -----------------
# Document
# -----------------
class Document(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    file = models.FileField(upload_to='lesson_documents/')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    source_links = models.TextField(blank=True, null=True)
    is_downloadable = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# -----------------
# Video
# -----------------
class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    video_file = models.FileField(upload_to='lesson_videos/', blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# -----------------
# Image
# -----------------
class Image(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image_file = models.ImageField(upload_to='lesson_images/', blank=True, null=True)
    image_link = models.URLField(blank=True, null=True)
    sort_order = models.IntegerField(default=0)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# -----------------
# Course Enrollment
# -----------------
class CourseEnrollment(models.Model):
    ENROLL_TYPE_CHOICES = [
        ('self_enrolled', 'Self Enrolled'),
        ('admin_allocated', 'Admin Allocated'),
        ('bulk_import', 'Bulk Import'),
    ]
    ENROLL_STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('suspended', 'Suspended'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_type = models.CharField(max_length=20, choices=ENROLL_TYPE_CHOICES)
    enrollment_status = models.CharField(max_length=20, choices=ENROLL_STATUS_CHOICES, default='active')
    enrolled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='enrolled_users'
    )
    enrollment_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    last_accessed = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# -----------------
# Lesson Progress
# -----------------
class LessonProgress(models.Model):
    PROGRESS_STATUS = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    enrollment = models.ForeignKey(CourseEnrollment, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PROGRESS_STATUS, default='not_started')
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    time_spent_seconds = models.IntegerField(default=0)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    last_accessed = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# -----------------
# Activity Log
# -----------------
class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    activity_type = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    additional_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity_type} - {self.user}"


# -----------------
# Upload
# -----------------
class Upload(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to="course_files/",
        validators=[
            FileExtensionValidator(
                ["pdf", "docx", "doc", "xls", "xlsx", "ppt", "pptx", "zip", "rar", "7zip"]
            )
        ],
    )
    updated_date = models.DateTimeField(auto_now=True)
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UploadVideo(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video = models.FileField(
        upload_to="course_videos/",
        validators=[FileExtensionValidator(["mp4", "mkv", "wmv", "3gp", "f4v", "avi", "mp3"])],
    )
    summary = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# -----------------
# Course Allocation (NEW FINAL VERSION)
# -----------------
class CourseAllocation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  # ✅ TEMPORARILY allow null
        blank=True
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        null=True,  # ✅ TEMPORARILY allow null
        blank=True
    )
    assigned_date = models.DateTimeField(default=timezone.now)  # ✅ avoids auto_now_add issue
    due_date = models.DateTimeField(null=True, blank=True)

    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} → {self.course}"
