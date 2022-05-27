from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from user.forms.profile_form import ProfileForm
from user.models import UserDetails;


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'pages/user/register.html', {
        'form': UserCreationForm()
    })


@login_required
def profile(request):
    user = UserDetails.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = ProfileForm(instance=user, data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect('profile')

    return render(request, 'pages/user/profile.html', {
        'form': ProfileForm(instance=user)
    })

