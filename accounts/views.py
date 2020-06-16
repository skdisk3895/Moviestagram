from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from reviews.forms import CommentForm

User = get_user_model()

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            auth_login(request, form.save())
            return redirect('home:home')
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'home:home')
        else:
            messages.error(request, '아이디 또는 비밀번호가 틀렸습니다.')
            return redirect('accounts:login')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

@require_GET
@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')

@require_GET
@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    comment_form = CommentForm()
    context = {
        'user': user,
        'comment_form': comment_form,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            username = request.user.username
            return redirect('accounts:profile', username)
        else:
            messages.error(request, '비밀번호가 다릅니다.')
            return redirect('accounts:update')
    else:
        form = PasswordChangeForm(request.POST)
    context = {
        'form' : form
    }
    return render(request, 'accounts/update.html', context)