from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser

from user.forms.profile_form import ProfileForm
from user.forms.user_info_form import UserInfoForm
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
            return redirect('/user/login')
        else:
            return render(request, 'pages/user/register.html', {
                'form': form
            })

    return render(request, 'pages/user/register.html', {
        'form': SignUpForm()
    })


@login_required
def profile(request):
    user_details = UserDetails.objects.filter(user=request.user).first()
    posting_failed = False

    if request.method == 'POST':
        # Posting user details form
        form = ProfileForm(instance=user_details, data=request.POST)
        if form.is_valid():
            user_details = form.save(commit=False)
            user_details.user = request.user
            user_details.save()
            return redirect('/user/profile?success=true')
        else:
            posting_failed = True

        # Posting user standard information form
        form2 = UserInfoForm(instance=request.user, data=request.POST)
        if form2.is_valid():
            user = form2.save(commit=False)
            user.save()
            return redirect('/user/profile?success=true')
        
        else:
            posting_failed = True

        if posting_failed:
            return render(request, 'pages/user/profile.html', {
                    'form': form,
                    'form2': form2,
                    'user_details': user_details,
                    'user': request.user
                })

    return render(request, 'pages/user/profile.html', {
        'form': ProfileForm(instance=user_details),
        'form2': UserInfoForm(instance=request.user),
        'user_details': user_details,
        'user': request.user
    })
