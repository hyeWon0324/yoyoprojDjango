from django import forms
#from .social_models import TrackPost
from .models import Posts, Tracks, Users


class PostForm(forms.ModelForm):

    class Meta:
       # model = TrackPost
        model = Posts
        fields = ('contents','tags', 'users_idx', 'track_idx')


class TrackForm(forms.ModelForm):

    class Meta:
        model = Tracks
        fields = ('title', 'moods', 'genre_idx')

