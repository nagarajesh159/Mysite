from .models import Question, Choice
from django.forms import ModelForm


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ("question_text",)


class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ("choice_text", "votes")
