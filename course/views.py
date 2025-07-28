from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Course, Lesson, Document, Video, Image, CourseEnrollment
from .forms import CourseForm, LessonForm
from .forms import DocumentForm, VideoForm, ImageForm
from django.views.generic import FormView
from course.models import LessonProgress
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt


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
        context['all_lessons'] = Lesson.objects.filter(course=lesson.course).order_by('sort_order')
        return context

class LessonStartView(DetailView):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect if user not logged in

        lesson = get_object_or_404(Lesson, pk=pk)

        # Get or create course enrollment for the user
        enrollment, _ = CourseEnrollment.objects.get_or_create(
            user=request.user,
            course=lesson.course
        )

        # Create or update LessonProgress
        progress, created = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            enrollment=enrollment,
            defaults={
                'status': 'in_progress',
                'started_at': timezone.now(),
                'last_accessed': timezone.now()
            }
        )

        if not created:
            # If it already exists, just update status and last accessed
            progress.status = 'in_progress'
            progress.last_accessed = timezone.now()
            progress.save()

        return redirect('lesson_detail_view', pk=lesson.pk)
    
class LessonFinishView(View):
    def post(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)

        # Get the user's enrollment for this course
        enrollment = CourseEnrollment.objects.filter(
            course=lesson.course,
            user=request.user
        ).first()

        if not enrollment:
            # Handle case: user is not enrolled
            return redirect('home')

        # Get or create lesson progress for this enrollment
        progress, created = LessonProgress.objects.get_or_create(
            lesson=lesson,
            enrollment=enrollment,
            user=request.user,
        )

        progress.status = 'completed'
        progress.completed_at = timezone.now()
        progress.save()

        return redirect(reverse('course_watch_view', args=[lesson.course.id]))

    
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















