from django.forms import ModelForm, widgets
from user.models import UserDetails
from home.models import City


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super (ProfileForm, self).__init__(*args,**kwargs) # populates the post
        self.fields['postal_city'].queryset = City.objects.filter(country=self.instance.postal_country)
    
    class Meta:
        model = UserDetails
        exclude = ['id', 'user']
        widgets = {
            'profile_image_url': widgets.TextInput(attrs={'class': 'form-control'})
        }
