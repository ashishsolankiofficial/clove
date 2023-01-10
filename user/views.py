from django.shortcuts import render, redirect, get_object_or_404
from user.forms import AdminForm, UserForm
from user.models import User
from office.models import Office
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def show_workflow(request):
    return render(request, 'workflow.html', {'user': request.user})


def admin_registration(request, ext_id=None):
    try:
        user_profile = User.objects.get(ext_id=ext_id)
    except:
        pass
    if request.method == 'POST':
        if ext_id:
            fm = AdminForm(request.POST or None, instance=user_profile)
        else:
            fm = AdminForm(request.POST)
        if fm.is_valid():
            user = fm.save(commit=False)
            user.set_password('admin')
            user.office_admin = True
            user.save()
            return redirect("admin_list")
    else:
        if ext_id:
            fm = AdminForm(instance=user_profile)
        else:
            fm = AdminForm()
    return render(request, 'admin_registration.html', {'form': fm})


def admin_list(request):
    admins = User.objects.filter(office_admin=True).all().values("ext_id", "display_name", "first_name", "last_name", "office__name")
    admin_list = {
        'admin_list': admins
    }
    return render(request, 'admin_list.html', admin_list)


def user_registration(request, ext_id=None):
    try:
        user_profile = User.objects.get(ext_id=ext_id)
    except:
        pass
    if request.method == 'POST':
        if ext_id:
            fm = UserForm(request.POST or None, instance=user_profile)
        else:
            fm = UserForm(request.POST)
        if fm.is_valid():
            user = fm.save(commit=False)
            user.office = Office.objects.get(name=request.user.office)
            user.set_password('admin')
            user.save()
            return redirect("user_list")
    else:
        if ext_id:
            fm = UserForm(instance=user_profile)
        else:
            fm = UserForm()
    return render(request, 'user_registration.html', {'form': fm})


def user_list(request):
    users = User.objects.filter(office__name=request.user.office).all().values("ext_id", "display_name", "first_name", "last_name")
    user_list = {
        'user_list': users
    }
    return render(request, 'user_list.html', user_list)


def login_admin(request):
    if request.user.is_authenticated:
        return redirect("workflow")
    if request.method == "POST":
        fm = AuthenticationForm(request, data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data.get('username')
            password = fm.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
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
