from django import forms
#from .social_models import TrackPost
from .models import Posts, Tracks, Users, Comments


class PostForm(forms.ModelForm):
    contents = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your description!'
    )

    class Meta:
       # model = TrackPost
        model = Posts
        fields = ('contents', 'tags', 'users_idx', 'track_idx')


class TrackForm(forms.ModelForm):

    class Meta:
        model = Tracks
        fields = ('title', 'type_idx', 'moods', 'genre_idx')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('users_idx', 'contents', )


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    source = forms.CharField(
        max_length=50,
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        message = cleaned_data.get('message')
        if not name and not message:
            raise forms.ValidationError('You have to write something!')
