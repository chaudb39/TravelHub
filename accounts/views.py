from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm


def register_view(request):
    theme = request.COOKIES.get('theme', 'light')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(request, 'Đăng ký tài khoản thành công.')
            return redirect('accounts:login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'theme': theme
    })


def login_view(request):
    theme = request.COOKIES.get('theme', 'light')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')

    return render(request, 'accounts/login.html', {
        'theme': theme
    })


def logout_view(request):
    logout(request)
    return redirect('core:home')


@login_required
def profile_view(request):
    theme = request.COOKIES.get('theme', 'light')

    return render(request, 'accounts/profile.html', {
        'theme': theme
    })


@login_required
def change_password_view(request):
    theme = request.COOKIES.get('theme', 'light')

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, 'Đổi mật khẩu thành công.')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {
        'form': form,
        'theme': theme
    })
