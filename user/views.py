from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
    user_details = UserDetails.objects.filter(user=request.user).first()

    print(user_details)

    if request.method == 'POST':
        form = ProfileForm(instance=user_details, data=request.POST)
        if form.is_valid():
            user_details = form.save(commit=False)
            user_details.user = request.user
            user_details.save()
            return redirect('profile')

    return render(request, 'pages/user/profile.html', {
        'form': ProfileForm(instance=user_details),
        'user_details': user_details,
        'user': request.user
    })

