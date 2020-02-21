
from ..models import Posts , Tracks, Users
from rest_framework import serializers


class TrackModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = [
            'idx',
            'title',
            'genre_idx',
            'type_idx',
            'track_source',
            'image',
            'flag',
            'users_idx',
            'created_dt',
            'played_count',
            'moods',
        ]


class PostModelSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()
    track_idx = TrackModelSerializer(read_only=True)
    did_like = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = [
            'idx',
            'contents',
            'users_idx',
            'created_dt',
            'track_idx',
            'tags',
            'comments_count',
            'likes_count',
            'updated_dt',
        ]

    def get_access(self):
        pass



    def get_did_like(self, obj):
        try:
            user = self.request.user
            if user.is_authenticated():
                if user in obj.liked.all():
                    return True
        except:
            pass
        return False

