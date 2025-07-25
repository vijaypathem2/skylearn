from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Course, Lesson, Document, Video, Image
from .forms import CourseForm, LessonForm
from .forms import DocumentForm, VideoForm, ImageForm
from django.views.generic import FormView


# -------------------- Course Views --------------------

class Course_Home_ListView(ListView):
    model = Course
    template_name = 'course/course_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context["title"] = course.title
        context["lessons"] = Lesson.objects.filter(course=course)
        return context


class CourseDetailWatchView(DetailView):
    model = Course
    template_name = "course/course_watchview.html"
    context_object_name = "course"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context["title"] = course.title
        context["lessons"] = Lesson.objects.filter(course=course)
        return context


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/course_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("lesson_create", kwargs={"pk": self.object.pk})


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/course_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('home')


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'course/course_confirm_delete.html'
    success_url = reverse_lazy('home')


# -------------------- Lesson Views --------------------

class CourseLessonListView(ListView):
    model = Lesson
    template_name = 'course/course_lessons.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        course_id = self.kwargs['pk']
        return Lesson.objects.filter(course_id=course_id).order_by('sort_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=self.kwargs['pk'])
        return context


class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "course/lesson_create.html"

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.course = self.course
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("course_detail", kwargs={"pk": self.course.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["course"] = self.course
        return ctx




class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'course/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        context['documents'] = Document.objects.filter(lesson=lesson)
        context['videos'] = Video.objects.filter(lesson=lesson)
        context['images'] = Image.objects.filter(lesson=lesson)
        return context
    
class LessonContentManageView(DetailView):
    model = Lesson
    template_name = "course/lesson_content_manage.html"
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Document.objects.filter(lesson=self.object)
        context['videos'] = Video.objects.filter(lesson=self.object)
        context['images'] = Image.objects.filter(lesson=self.object)
        context['document_form'] = DocumentForm()
        context['video_form'] = VideoForm()
        context['image_form'] = ImageForm()
        return context



class DocumentCreateView(CreateView):
    model = Document
    fields = ['title', 'file', 'description']
    template_name = 'course/add_document.html'

    def dispatch(self, request, *args, **kwargs):
        self.lesson = get_object_or_404(Lesson, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.lesson = self.lesson
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lesson_manage', kwargs={'pk': self.lesson.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = self.lesson
        return context


class VideoCreateView(CreateView):
    model = Video
    fields = ['title', 'video_file', 'video_link', 'description']
    template_name = 'course/add_video.html'

    def dispatch(self, request, *args, **kwargs):
        self.lesson = get_object_or_404(Lesson, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.lesson = self.lesson
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lesson_manage', kwargs={'pk': self.lesson.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = self.lesson
        return context


class ImageCreateView(CreateView):
    model = Image
    fields = ['title', 'image_file', 'image_link', 'description']
    template_name = 'course/add_image.html'

    def dispatch(self, request, *args, **kwargs):
        self.lesson = get_object_or_404(Lesson, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.lesson = self.lesson
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lesson_manage', kwargs={'pk': self.lesson.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = self.lesson
        return context










# class DocumentCreateView(CreateView):
#     model = Document
#     fields = ['title', 'file', 'description']
#     template_name = 'course/add_document.html'

#     def form_valid(self, form):
#         form.instance.lesson_id = self.kwargs['pk']
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('lesson_manage', kwargs={'pk': self.kwargs['pk']})


# class VideoCreateView(CreateView):
#     model = Video
#     fields = ['title', 'video_file', 'video_link', 'description']
#     template_name = 'course/add_video.html'

#     def form_valid(self, form):
#         form.instance.lesson_id = self.kwargs['pk']
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('lesson_manage', kwargs={'pk': self.kwargs['pk']})


# class ImageCreateView(CreateView):
#     model = Image
#     fields = ['title', 'image_file', 'image_link', 'description']
#     template_name = 'course/add_image.html'

#     def form_valid(self, form):
#         form.instance.lesson_id = self.kwargs['pk']
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('lesson_manage', kwargs={'pk': self.kwargs['pk']})










# from django.conf import settings
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator
# from django.shortcuts import get_object_or_404, redirect, render
# from django.utils.decorators import method_decorator
# from .models import Course, Lesson

# from accounts.decorators import lecturer_required, student_required
# from accounts.models import Student
# from core.models import Semester
# from course.forms import (
#     UploadFormFile,
#     UploadFormVideo,
# )
# from course.models import (
#     Course,
#     Video,
#     Image,
#     Department,
#     Lesson,
#     Document,
#     CourseEnrollment,
#     LessonProgress,
#     ActivityLog,
# )
# from result.models import TakenCourse
# from assessments.models import Assessment
# from .forms import CourseForm, LessonForm
# from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
# from django.urls import reverse_lazy
# from .views import LessonDetailView


# class Course_Home_ListView(ListView):
#     model = Course
#     template_name = 'course/course_list.html'
#     context_object_name = 'courses'


# class CourseDetailView(DetailView):
#     model = Course
#     template_name = 'course/course_detail.html'
#     context_object_name = 'course'

#     def get_queryset(self):
#         return Course.objects.filter(status='published')


# class CourseDetailWatchView(DetailView):
#     model = Course
#     template_name = "course/course_watchview.html"
#     context_object_name = "course"
#     pk_url_kwarg = "pk"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         course = self.get_object()
#         context["title"] = course.title
#         context["lessons"] = Lesson.objects.filter(course=course)
#         return context


# class LessonView(DetailView):
#     model = Lesson
#     template_name = 'course/lesson_detail.html'
#     context_object_name = 'lesson'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         lesson = self.get_object()
#         context['documents'] = Document.objects.filter(lesson=lesson)
#         context['videos'] = Video.objects.filter(lesson=lesson)
#         context['images'] = Image.objects.filter(lesson=lesson)
#         return context


# class CourseCreateView(CreateView):
#     model = Course
#     form_class = CourseForm
#     template_name = 'course/course_create.html'
#     success_url = reverse_lazy('home')

#     def form_valid(self, form):
#         form.instance.added_by = self.request.user
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return reverse("lesson_create", kwargs={"course_pk": self.object.pk})


# class CourseDeleteView(DeleteView):
#     model = Course
#     template_name = 'course/course_confirm_delete.html'
#     success_url = reverse_lazy('home')


# class CourseUpdateView(UpdateView):
#     model = Course
#     form_class = CourseForm
#     template_name = 'course/course_update.html'
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'
#     success_url = reverse_lazy('home')


# class CourseLessonListView(ListView):
#     model = Lesson
#     template_name = 'course/course_lessons.html'
#     context_object_name = 'lessons'

#     def get_queryset(self):
#         course_id = self.kwargs['pk']
#         return Lesson.objects.filter(course_id=course_id).order_by('sort_order')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['course'] = Course.objects.get(pk=self.kwargs['pk'])
#         return context
    
# class LessonCreateView(CreateView):
#     model = Lesson
#     form_class = LessonForm
#     template_name = "course/lesson_create.html"

#     def dispatch(self, request, *args, **kwargs):
#         self.course = get_object_or_404(Course, pk=kwargs["course_pk"])
#         return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         form.instance.course = self.course
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse("course_lessons", kwargs={"pk": self.course.pk})

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx["course"] = self.course
#         return ctx
    
# class LessonDetailView(DetailView):
#     model = Lesson
#     template_name = 'course/lesson_detail.html'
#     context_object_name = 'lesson'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         lesson = self.get_object()
#         context['documents'] = Document.objects.filter(lesson=lesson)
#         context['videos'] = Video.objects.filter(lesson=lesson)
#         context['images'] = Image.objects.filter(lesson=lesson)
#         return context









# from django.conf import settings
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator
# from django.shortcuts import get_object_or_404, redirect, render
# from django.utils.decorators import method_decorator
# # from django.utils.text import slugify
# # import uuid

# from accounts.decorators import lecturer_required, student_required
# from accounts.models import Student
# from core.models import Semester
# from course.forms import (
#     UploadFormFile,
#     UploadFormVideo,
# )
# from course.models import (
#     Course,
#     Video,
#     Image,
#     Department,
#     Lesson,
#     Document,
#     CourseEnrollment,
#     LessonProgress,
#     ActivityLog,
# )
# from result.models import TakenCourse
# from assessments.models import Assessment
# from .forms import CourseForm
# from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
# from django.urls import reverse_lazy


# class Course_Home_ListView(ListView):
#     model = Course
#     template_name = 'course/course_list.html'
#     context_object_name = 'courses'

# class CourseDetailView(DetailView):
#     model = Course
#     template_name = 'course/course_detail.html'
#     context_object_name = 'course'

#     def get_queryset(self):
#         return Course.objects.filter(status='published')  # Optional filter
    
# class CourseDetailWatchView(DetailView):
#     model = Course
#     template_name = "course/course_watchview.html"
#     context_object_name = "course"
#     pk_url_kwarg = "pk"  
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         course = self.get_object()
#         context["title"] = course.title
#         context["lessons"] = Lesson.objects.filter(course=course)
#         return context
    

# class LessonView(DetailView):
#     model = Lesson
#     template_name = 'course/lesson_detail.html'
#     context_object_name = 'lesson'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         lesson = self.get_object()

#         context['documents'] = Document.objects.filter(lesson=lesson)
#         context['videos'] = Video.objects.filter(lesson=lesson)
#         context['images'] = Image.objects.filter(lesson=lesson)

#         return context

    
# class CourseCreateView(CreateView):
#     model = Course
#     form_class = CourseForm
#     template_name = 'course/course_create.html'
#     success_url = reverse_lazy('home')

#     def form_valid(self, form):
#         form.instance.added_by = self.request.user  # Optional: Set current user as creator
#         return super().form_valid(form)

# class CourseDeleteView(DeleteView):
#     model = Course
#     template_name = 'course/course_confirm_delete.html'
#     success_url = reverse_lazy('home')

# class CourseUpdateView(UpdateView):
#     model = Course
#     form_class = CourseForm
#     template_name = 'course/course_update.html'
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'
#     success_url = reverse_lazy('home')

# class CourseLessonView(ListView):
#     model = Lesson
#     template_name = 'course/course_lessons.html'
#     context_object_name = 'lessons'

#     def get_queryset(self):
#         course_id = self.kwargs['pk']
#         return Lesson.objects.filter(course_id=course_id)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['course'] = Course.objects.get(pk=self.kwargs['pk'])
#         return context

