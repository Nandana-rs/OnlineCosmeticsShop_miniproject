# forms.py
from django import forms
from .models import Video

from .models import Beautician


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']



class BeauticianProfileForm(forms.ModelForm):
    class Meta:
        model = Beautician
        fields = ['bio', 'phone_number', 'address', 'website', 'social_media_links',
                  'experience_years', 'certifications', 'availability']

