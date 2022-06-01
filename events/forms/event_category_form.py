from faulthandler import disable
from django.forms import ModelForm, widgets
from home.models import EventCategory


class EventCategory(ModelForm):
    class Meta:
        model = EventCategory
        exclude = ['id']
        # disable the event field
        widgets = {
            'event': widgets.HiddenInput(),
        }
        # widgets = {
        #     'category': widgets.CheckboxSelectMultiple(),

        # }
