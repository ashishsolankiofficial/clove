from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect, get_object_or_404
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


def show_workflow(request):
    return render(request, 'workflow.html', {'user': request.user})


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
    return render(request, 'add_admin.html', {'form': fm})


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
    return render(request, 'add_admin.html', {'form': fm})


def list_admin(request):
    admins = User.objects.filter(office_admin=True).all().values("ext_id", "display_name", "first_name", "last_name", "office__name")
    admin_list = {
        'admin_list': admins
    }
    return render(request, 'list_admin.html', admin_list)


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
    return render(request, 'add_user.html', {'form': fm})


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
    return render(request, 'add_user.html', {'form': fm})


def list_user(request):
    users = User.objects.filter(office__name=request.user.office).all().values("ext_id", "display_name", "first_name", "last_name")
    user_list = {
        'user_list': users
    }
    return render(request, 'list_user.html', user_list)


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
    return render(request, 'admin_login.html', {'form': fm})


def logout_admin(request):
    logout(request)
    return redirect('admin_login')
