from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView 
from .forms import QuestionForm, OptionForm
from django.shortcuts import redirect

from django.urls import reverse_lazy
from .models import Department, Assessment, Question, Option, AssessmentAttempt, UserResponse

class DepartmentListView(ListView):
    model = Department
    template_name = 'department/list.html'
    context_object_name = 'departments'

class DepartmentCreateView(CreateView):
    model = Department
    fields = ['name']
    template_name = 'department/form.html'
    success_url = reverse_lazy('department_list')


class AssessmentListView(ListView):
    model = Assessment
    template_name = 'assessments/assessment_list.html'
    context_object_name = 'assessments'

class AssessmentDetailView(DetailView):
    model = Assessment
    template_name = 'assessments/assessment_detail.html'
    context_object_name = 'assessment'

class AssessmentCreateView(CreateView):
    model = Assessment
    fields = ['department', 'title', 'description', 'created_by', 'duration_minutes', 'total_questions', 'passing_score', 'is_active']
    template_name = 'assessments/assessment_create.html'
    success_url = reverse_lazy('assessment_list')

class AssessmentUpdateView(UpdateView):
    model = Assessment
    fields = ['department', 'title', 'description', 'duration_minutes', 'total_questions', 'passing_score', 'is_active']
    template_name = 'assessments/assessment_update.html'
    success_url = reverse_lazy('assessment_list')

class AssessmentDeleteView(DeleteView):
    model = Assessment
    template_name = 'assessments/assessment_confirm_delete.html'
    success_url = reverse_lazy('assessment_list')


class QuestionListView(ListView):
    model = Question
    template_name = 'assessments/question/list.html'
    context_object_name = 'questions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['option_form'] = OptionForm()
        return context

    def post(self, request, *args, **kwargs):  # ← line 60
        form = OptionForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('question_list')



class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'question/form.html'

    def get_initial(self):
        initial = super().get_initial()
        assessment_id = self.kwargs.get('assessment_id')
        if assessment_id:
            initial['assessment'] = assessment_id
        return initial

    def form_valid(self, form):
        assessment = form.cleaned_data['assessment']
        total_questions = assessment.total_questions
        form.instance.duration = (
            assessment.duration_minutes / total_questions if total_questions > 0 else 0
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from assessments.models import Assessment
        context['assessment_data'] = [
            {
                'id': assessment.id,
                'duration_minutes': assessment.duration_minutes,
                'total_questions': assessment.total_questions,
            }
            for assessment in Assessment.objects.all()
        ]
        return context

    def get_success_url(self):
        return reverse('question_list')  # or any redirect you prefer



# class OptionListView(ListView):
#     model = Option
#     template_name = 'option/list.html'
#     context_object_name = 'options'

class OptionCreateView(CreateView):
    model = Option
    fields = ['assessment', 'question', 'option_text', 'option_letter', 'is_correct']
    template_name = 'option/form.html'
    success_url = reverse_lazy('option_list')


class AssessmentAttemptListView(ListView):
    model = AssessmentAttempt
    template_name = 'attempt/list.html'
    context_object_name = 'attempts'

class AssessmentAttemptDetailView(DetailView):
    model = AssessmentAttempt
    template_name = 'attempt/detail.html'
    context_object_name = 'attempt'


class UserResponseListView(ListView):
    model = UserResponse
    template_name = 'response/list.html'
    context_object_name = 'responses'

class UserResponseCreateView(CreateView):
    model = UserResponse
    fields = ['attempt', 'question', 'selected_option', 'is_correct']
    template_name = 'response/form.html'
    success_url = reverse_lazy('response_list')
