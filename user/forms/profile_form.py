from django.forms import ModelForm, widgets
from user.models import UserDetails


class ProfileForm(ModelForm):
    class Meta:
        model = UserDetails
        exclude = ['id', 'user']
        widgets = {
            'profile_image_url': widgets.TextInput(attrs={'class': 'form-control'})
        }
