from django import forms
from .models import Question, Option

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['assessment', 'question_text', 'question_number', 'is_active', 'duration']
        widgets = {
            'duration': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['assessment', 'question', 'option_text', 'option_letter', 'is_correct']
        widgets = {
            'assessment': forms.HiddenInput(),
            'question': forms.HiddenInput(),
        }
