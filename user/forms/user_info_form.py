from django.forms import ModelForm, widgets
from django.contrib.auth.models import User


class UserInfoForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        # exclude = ['id', 'password', 'last_login', 'is_superuser', 'username', 'is_staff', 'is_active', 'date_joined']
