
from django.urls import path

from . import views

app_name = "storeapp"

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.sign_up, name='signup'),
    path('signup/<str:person>', views.signup2, name='signup2'),
    path('login/', views.login_in, name='login'),
    path('logout/', views.logout_out, name='logout'),
    path('create-task/', views.create_task, name='createtask'),
    path('assign-task/', views.assign_task, name='assigntask'),
    path('task/<int:task_id>/assign/', views.accept_task, name='accept-task'),
    path('change-task-status/', views.change_task_status, name='change-task-status'),
    path('change-task-status/<int:task_id>/', views.change_status, name='change-status'),
]
