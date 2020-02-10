from django import forms
#from .social_models import TrackPost
from .models import Posts, Tracks

class PostForm(forms.ModelForm):

    class Meta:
       # model = TrackPost
        model = Posts
        fields = ('contents',)
