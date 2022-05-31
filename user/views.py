from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser

from user.forms.profile_form import ProfileForm
from user.models import UserDetails
from user.forms.sign_up_form import SignUpForm

def get_user_details(user):
    if isinstance(user, AnonymousUser):
        user_details = None
    else:
        user_details = UserDetails.objects.filter(user=user).first()
    
    return user_details

def register(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'pages/user/register.html', {
        'form': SignUpForm()
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

