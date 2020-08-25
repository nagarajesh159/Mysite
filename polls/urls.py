from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.get_question, name='get-question'),
    path('validate/question/', views.validate_question, name='validate-question'),
    path('<int:question_id>/add-choice/', views.add_choice, name='add-choice'),
    path('<int:question_id>/votes/', views.votes, name='add-vote'),
]
