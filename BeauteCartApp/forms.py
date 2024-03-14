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
        

# forms.py

from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'start_time', 'end_time', 'location', 'special_requests']

# from .models import CustomizeBooking

# class CustomizeBookingForm(forms.ModelForm):
#     class Meta:
#         model = CustomizeBooking
#         fields = '__all__'

# from django import forms
from .models import CustomizeBooking

class CustomizeBookingForm(forms.ModelForm):
    class Meta:
        model = CustomizeBooking
        fields = ['name', 'phone', 'location', 'email', 'makeup_type', 'budget', 'event_date', 'specific_requirements']



#nandana blog
        
from .models import Post       
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']