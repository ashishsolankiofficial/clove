from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.forms import AdminForm, UserForm
from user.models import User
from user.serializer import UserProfileSerializer
from payable.models import PayableProfile
from office.models import Office
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class UserProfileView(APIView):
    def get(self, request, ext_id):
        profile = User.objects.get(ext_id=ext_id)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, ext_id, format=None):
        profile = User.objects.get(ext_id=ext_id)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    def post(self, request):
        username = request.user.email
        old_password = request.data['old_password']
        password = request.data['password']
        password2 = request.data['password2']
        if password != password2:
            return Response('New Passwords Do not Match', status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=old_password)
        if user is not None:
            user.set_password(password)
            user.save()
            return Response('Password updated successfully', status.HTTP_200_OK)
        else:
            return Response('Invalid Old Password', status=status.HTTP_400_BAD_REQUEST)


def show_workflow(request):
    return render(request, 'user/workflow.html', {'user': request.user})


def add_admin(request, ext_id=None):
    if request.method == 'POST':
        fm = AdminForm(request.POST)
        if fm.is_valid():
            user = fm.save(commit=False)
            user.set_password('admin')
            user.office_admin = True
            user.save()
            PayableProfile.objects.create(user=user)
            return redirect("list_admin")
    else:
        fm = AdminForm()
    return render(request, 'user/add_admin.html', {'form': fm})


def edit_admin(request, ext_id):
    user_profile = get_object_or_404(User, ext_id=ext_id)
    if request.method == 'POST':
        fm = AdminForm(request.POST, instance=user_profile)
        if fm.is_valid():
            user = fm.save(commit=False)
            user.set_password('admin')
            user.office_admin = True
            user.save()
            return redirect("list_admin")
    else:
        fm = AdminForm(instance=user_profile)
    return render(request, 'user/add_admin.html', {'form': fm})


def list_admin(request):
    admins = User.objects.filter(office_admin=True, is_active=True).all().values("ext_id", "display_name", "first_name", "last_name", "office__name", "email")
    page = request.GET.get('page', 1)
    paginator = Paginator(admins, 10)
    try:
        admins = paginator.page(page)
    except PageNotAnInteger:
        admins = paginator.page(1)
    except EmptyPage:
        admins = paginator.page(paginator.num_pages)
    admin_list = {
        'admin_list': admins
    }
    return render(request, 'user/list_admin.html', admin_list)


def list_inactive_admin(request):
    admins = User.objects.filter(office_admin=True, is_active=False).all().values("ext_id", "display_name", "first_name", "last_name", "office__name", "email")
    page = request.GET.get('page', 1)
    paginator = Paginator(admins, 10)
    try:
        admins = paginator.page(page)
    except PageNotAnInteger:
        admins = paginator.page(1)
    except EmptyPage:
        admins = paginator.page(paginator.num_pages)
    admin_list = {
        'admin_list': admins
    }
    return render(request, 'user/list_inactive_admin.html', admin_list)


def add_user(request):
    if request.method == 'POST':
        fm = UserForm(request.POST)
        if fm.is_valid():
            user = fm.save(commit=False)
            user.office = Office.objects.get(name=request.user.office)
            user.set_password('admin')
            user.save()
            PayableProfile.objects.create(user=user)
            return redirect("list_user")
    else:
        fm = UserForm()
    return render(request, 'user/add_user.html', {'form': fm})


def edit_user(request, ext_id):
    user_profile = get_object_or_404(User, ext_id=ext_id)
    if request.method == 'POST':
        fm = UserForm(request.POST, instance=user_profile)
        if fm.is_valid():
            user = fm.save(commit=False)
            user.office = Office.objects.get(name=request.user.office)
            user.set_password('admin')
            user.save()
            return redirect("list_user")
    else:
        fm = UserForm(instance=user_profile)
    return render(request, 'user/add_user.html', {'form': fm})


def list_user(request):
    users = User.objects.filter(office__name=request.user.office, is_active=True).all().values("ext_id", "display_name", "first_name", "last_name", "email")
    page = request.GET.get('page', 1)
    paginator = Paginator(users, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    user_list = {
        'user_list': users
    }
    return render(request, 'user/list_user.html', user_list)


def list_inactive_user(request):
    users = User.objects.filter(office__name=request.user.office, is_active=False).all().values("ext_id", "display_name", "first_name", "last_name", "email")
    page = request.GET.get('page', 1)
    paginator = Paginator(users, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    user_list = {
        'user_list': users
    }
    return render(request, 'user/list_inactive_user.html', user_list)


def login_admin(request):
    if request.user.is_authenticated:
        return redirect("workflow")
    if request.method == "POST":
        fm = AuthenticationForm(request, data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data.get('username')
            password = fm.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if not (user.office_admin or user.is_superuser):
                messages.error(request, "Portal is only for OfficeJAM Administrators")
                return redirect("admin_login")
            if user is not None:
                login(request, user)
                return redirect("workflow")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    fm = AuthenticationForm()
    return render(request, 'user/admin_login.html', {'form': fm})


def logout_admin(request):
    logout(request)
    return redirect('admin_login')
