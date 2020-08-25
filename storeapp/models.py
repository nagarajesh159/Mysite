from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class StoreManager(models.Model):

    store_name = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=25)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DeliveryPerson(models.Model):
    name = models.CharField(max_length=25)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Task(models.Model):
    status_choices = (
        ('new', 'new'),
        ('accepted', "accepted"),
        ('completed', 'completed'),
        ('declined', 'declined')
    )

    priority_choices = (
        ('high', 'high'),
        ('medium', 'medium'),
        ('low', 'low'),
    )

    title = models.CharField(max_length=25)
    status = models.CharField(max_length=10, choices=status_choices)
    priority = models.CharField(max_length=10, choices=priority_choices)
    created_by = models.CharField(max_length=50)
    store_manager = models.ForeignKey(StoreManager, on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.title
