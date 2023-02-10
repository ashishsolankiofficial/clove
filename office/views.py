from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.models import User
from office.models import Task, Office
from office.forms import TaskForm
from office.serializer import TaskSerializer
from payable.models import PayableProfile
from payable.serializer import PayableProfileSerializer


class LeaderBoardView(APIView):
    def get(self, request):
        user = User.objects.get(ext_id=request.user.ext_id)
        profile = PayableProfile.objects.filter(user__office__ext_id=user.office.ext_id)
        serializer = PayableProfileSerializer(profile, many=True)
        return Response(serializer.data)


class TaskView(APIView):
    def get(self, request):
        user = User.objects.get(ext_id=request.user.ext_id)
        tasks = Task.objects.filter(office=user.office, active=True)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


def add_task(request):
    if request.method == 'POST':
        fm = TaskForm(request.POST)
        if fm.is_valid():
            task = fm.save(commit=False)
            task.office = User.objects.get(ext_id=request.user.ext_id).office
            task.save()
            return redirect("list_task")
    else:
        fm = TaskForm()
    return render(request, 'office/add_task.html', {'form': fm})


def edit_task(request, ext_id):
    task = get_object_or_404(Task, ext_id=ext_id)
    if request.method == 'POST':
        fm = TaskForm(request.POST, instance=task)
        if fm.is_valid():
            fm.save()
            return redirect("list_task")
    else:
        fm = TaskForm(instance=task)
    return render(request, 'office/add_task.html', {'form': fm})


def list_task(request):
    user = User.objects.get(ext_id=request.user.ext_id)
    tasks = Task.objects.filter(office=user.office)
    page = request.GET.get('page', 1)
    paginator = Paginator(tasks, 10)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    task_list = {
        'task_list': tasks
    }
    return render(request, 'office/list_task.html', task_list)
