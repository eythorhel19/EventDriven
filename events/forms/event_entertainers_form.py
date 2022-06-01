from faulthandler import disable
from django.forms import ModelForm, widgets
from home.models import EventEntertainer


class EventEntertainer(ModelForm):
    class Meta:
        model = EventEntertainer
        exclude = ['id']
        # disable the event field
        widgets = {
            'event': widgets.HiddenInput(),
        }
        # widgets = {
        #     'category': widgets.CheckboxSelectMultiple(),

        # }
