from django.contrib import admin
from .models import (
    Department,
    Course,
    Lesson,
    Document,
    Video,
    Image,
    CourseEnrollment,
    LessonProgress,
    ActivityLog,
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_of_department', 'is_active', 'created_at')
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'level', 'status', 'added_by', 'created_at')
    search_fields = ('title', 'short_description')
    list_filter = ('status', 'level', 'department')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'lesson_type', 'sort_order', 'is_preview', 'is_mandatory')
    search_fields = ('title', 'description')
    list_filter = ('lesson_type', 'is_preview', 'is_mandatory')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'is_downloadable', 'sort_order', 'uploaded_by', 'created_at')
    search_fields = ('title', 'description')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'sort_order', 'created_at')
    search_fields = ('title', 'description')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'sort_order', 'uploaded_by', 'created_at')
    search_fields = ('title', 'description')


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrollment_type', 'enrollment_status', 'progress_percentage', 'enrollment_date')
    search_fields = ('user__username', 'course__title')
    list_filter = ('enrollment_type', 'enrollment_status')


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'status', 'progress_percentage', 'time_spent_seconds')
    list_filter = ('status',)


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'ip_address', 'created_at')
    search_fields = ('activity_type', 'description', 'ip_address')
    list_filter = ('activity_type',)

















# from django.contrib import admin
# from django.contrib.auth.models import Group

# from .models import Program, Course, CourseAllocation, Upload
# from modeltranslation.admin import TranslationAdmin

# class ProgramAdmin(TranslationAdmin):
#     pass
# class CourseAdmin(TranslationAdmin):
#     pass
# class UploadAdmin(TranslationAdmin):
#     pass

# admin.site.register(Program, ProgramAdmin)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(CourseAllocation)
# admin.site.register(Upload, UploadAdmin)
