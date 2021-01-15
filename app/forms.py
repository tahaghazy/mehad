from django import forms
from .models import *

class NewOrder(forms.ModelForm):
    class Meta:
        model = OrderTow
        fields = [
            'quantity',
            'time',
            'full_name',
            'email',
            'phone',
            'address',
            'content',
        ]

