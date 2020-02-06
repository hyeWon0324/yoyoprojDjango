from django import forms


class PostForm(forms.ModelForm):

    class Meta:
        fields = ('title', 'type', 'genre', 'tags', 'description', 'image')