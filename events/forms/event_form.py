from django.forms import ModelForm, widgets
from events.models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['id']
        widgets = {
            'start_date': widgets.NumberInput(attrs={'type': 'date'}),
            'end_date': widgets.NumberInput(attrs={'type': 'date'}),
            'description': widgets.Textarea(attrs={'rows': 3}),
        }
