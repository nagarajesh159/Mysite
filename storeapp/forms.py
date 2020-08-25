from django import forms
from django.contrib.auth.models import User
from .models import StoreManager, Task, DeliveryPerson


class StoreManagerForm(forms.ModelForm):
    class Meta:
        model = StoreManager
        fields = ['name','store_name']


class DeliveryPersonForm(forms.ModelForm):
    class Meta:
        model = DeliveryPerson
        fields = ['name', ]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'priority']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']