from faulthandler import disable
from django.forms import ModelForm, widgets
from home.models import EventTicketTypePrice


class EventTicketTypePriceForm(ModelForm):
    class Meta:
        model = EventTicketTypePrice
        exclude = ['id']
        # disable the event field
        widgets = {
            'event': widgets.HiddenInput(),
        }
