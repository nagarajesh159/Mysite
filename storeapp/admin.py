from django.contrib import admin
from .models import StoreManager, DeliveryPerson, Task

# Register your models here.
admin.site.register(StoreManager)
admin.site.register(DeliveryPerson)
admin.site.register(Task)