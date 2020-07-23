from django.forms import ModelForm
from .models import ShortenedLink


class ShortenLinkForm(ModelForm):
    class Meta:
        model = ShortenedLink
        fields = [
            'special_name',
            'original_link'
        ]
