from django import forms
from .models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'rating-input'})