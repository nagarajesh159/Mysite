from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from .models import Question, Choice
from .forms import QuestionForm

import json
from django.core import serializers

# Create your views here.


def index(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))

    form = QuestionForm()
    question_list = Question.objects.all()
    print(question_list)
    return render(request, 'polls/index.html', {"question_list": question_list, "form": form})


def validate_question(request):
    question_text = request.GET.get('question_text', None)
    data = {
        'is_taken': Question.objects.filter(question_text__iexact=question_text).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Question already exists in the database'
    return JsonResponse(data)


def get_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/get-question.html', {"question": question})


def add_choice(request, question_id):

    question = get_object_or_404(Question, id=question_id)
    try:
        new_choice = question.choice_set.create(
            choice_text=request.POST['choice_text'],
        )
        print(new_choice.id)
        obj = Choice.objects.get(id=new_choice.id)
        dct = {
            'id': obj.id,
            'choice_text': obj.choice_text,
            'votes': obj.votes,
        }
        json_object = json.dumps(dct, indent=4)
        print(obj)

        return JsonResponse(dct)
    except:
        # dct = {
        #         #     "msg": 'error in adding the choice check whether the choice is present for the current question'
        #         # }
        json_object = json.dumps('error in adding the choice check whether the choice is present for the current '
                                 'question')

        return JsonResponse(json_object)


def votes(request, question_id):

    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choice_set.get(id=request.POST['radioValue'])
        selected_choice.votes += 1
        selected_choice.save()
        dct = {
            'id': selected_choice.id,
            'choice_text': selected_choice.choice_text,
            'votes': selected_choice.votes,
        }
        json_object = json.dumps(dct, indent=4)
        print(selected_choice)

        return JsonResponse(dct)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return HttpResponse({'error': "invalid "})