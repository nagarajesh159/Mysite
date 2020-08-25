from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User

from .models import Task, StoreManager, DeliveryPerson
from .forms import StoreManagerForm, TaskForm, DeliveryPersonForm, UserForm

# Create your views here.


def index(request):
    return render(request, 'storeapp/index.html')


def sign_up(request):
    if request.method == 'POST':
        person = request.POST['person']
        return HttpResponseRedirect(reverse('storeapp:signup2', args=(person,)))
    return render(request, 'storeapp/signup.html')


# def signup2(request, person):
#     # print(person)
#
#     if request.method == "POST":
#         form = eval(person + 'Form()')
#         print(form['name'])
#         pass
#         # person = eval(person+'Form(request.POST)')
#     #     print(person)
#     form = eval(person + 'Form()')
#
#     return render(request, 'storeapp/signup2.html', {'form': form})


def signup2(request, person):
    userform = UserForm()

    if person == 'StoreManager':
        if request.method == 'POST':
            form = StoreManagerForm(request.POST)
            user = User.objects.create(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],
            )
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect(reverse('storeapp:index'))

        form = StoreManagerForm()
        return render(request, 'storeapp/signup2.html', {'form': form, 'userform': userform})
    elif person == 'DeliveryPerson':
        if request.method == 'POST':
            form = DeliveryPersonForm(request.POST)
            user = User.objects.create(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],
            )
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect(reverse('storeapp:index'))

        form = DeliveryPersonForm()
        return render(request, 'storeapp/signup2.html', {'form': form, 'userform': userform})
    else:
        return Http404


def login_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            try:
                manager = get_object_or_404(StoreManager, user=user)
                return HttpResponseRedirect(reverse('storeapp:createtask'))
            except:
                pass
            try:
                person = get_object_or_404(DeliveryPerson, user=user)
                return HttpResponseRedirect(reverse('storeapp:assigntask'))
            except:
                pass


        else:
            return render(request, 'storeapp/login.html')
    return render(request, 'storeapp/login.html')


def logout_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('storeapp:login'))


@login_required(login_url='login')
def create_task(request):
    user = request.user
    try:
        manager = get_object_or_404(StoreManager, user=user)
        if request.method == "POST":
            import pdb;pdb.set_trace()
            form = TaskForm(request.POST)
            task = form.save(commit=False)
            task.status = 'new'
            task.store_manager = manager
            task.created_by = manager.name
            task.save()
            return HttpResponseRedirect(reverse('storeapp:index'))
        form = TaskForm()
        return render(request, 'storeapp/create-task.html', {'form': form})
    except:
        return HttpResponse('failed')


@login_required(login_url='login')
def assign_task(request):
    user = request.user
    try:
        person = get_object_or_404(DeliveryPerson, user=user)
        task = Task.objects.filter(status='new')
        old_task = Task.objects.exclude(status='new')
        return render(request, 'storeapp/assign-task.html', {'task_list': task, "old_task": old_task})
    except:
        return HttpResponse('failed')


@login_required(login_url='login')
def accept_task(request, task_id):
    # import pdb; pdb.set_trace()
    task = get_object_or_404(Task, id=task_id)
    user = request.user
    form = TaskForm(instance=task)

    if task.status == 'new':
        try:
            person = get_object_or_404(DeliveryPerson, user=user)
            if person.count < 4:
                person.count += 1
                person.save()
                var = form.save(commit=False)
                var.status = 'accepted'
                var.delivery_person = person
                var.save()
                return HttpResponse(task, person)
            return HttpResponseRedirect(reverse('storeapp:assigntask'))
        except:
            return Http404
    return HttpResponse('failed')


@login_required(login_url='login')
def change_task_status(request):
    user = request.user
    try:
        person = get_object_or_404(DeliveryPerson, user=user)
        task_list = person.task_set.all()
        if request.method == "POST":
            return HttpResponse('Success')
        return render(request, "storeapp/change-task-status.html", {'task_list': task_list})
    except:
        return HttpResponse('Failed')


@login_required(login_url='login')
def change_status(request, task_id):
    user = request.user
    try:
        person = get_object_or_404(DeliveryPerson, user=user)
        task = get_object_or_404(Task, id=task_id)
        if request.method == "POST":

            status = request.POST['status']
            obj = Task.objects.filter(status='accepted').values('status').annotate(count=Count('id'))
            person.count = obj[0]['count']
            person.save()
            task.status = status
            task.save()
            return HttpResponseRedirect(reverse('storeapp:change-task-status'))
        return render(request, "storeapp/change-status.html", {'task': task})
    except:
        return HttpResponse('Failed')
