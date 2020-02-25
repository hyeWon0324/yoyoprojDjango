from django.utils.timesince import timesince
from ..models import Posts, Tracks, Users, Posts, Tracks, Likes, Comments
from rest_framework import serializers
import json


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


class TrackPostModelSerializer(serializers.ModelSerializer):
    #access_token = serializers.SerializerMethodField()
    track_idx = TrackModelSerializer(read_only=True)
    did_like = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    created_dt = serializers.SerializerMethodField()

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
            'did_like',
        ]

    # def get_access(self):
    #     pass


    def get_did_like(self, obj):
        try:
            user = self.request.user
            if user.is_authenticated():
                if user in obj.liked.all():
                    return True
        except:
            pass
        return False

    def get_tags(self, obj):
        try:
            hashtag_list = []
            if (obj.tags):
                taglist = obj.tags.split(' ')

                for tag in taglist:
                    hashtag_list.append("#" + tag)
            pass
        except:
            pass
        return hashtag_list

    def get_created_dt(self, obj):
        try:
            return timesince(obj.timestamp) + " ago"
        except:
            pass




# track post 작은 카드 버젼
class UsersDisplaySmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'idx',
            'user_id',
            'nickname',
            'profile_pic',
            'user_pic',
            'follower_count',
            'following_count',
            'tracks_count',
            'grade',
            'status',
            # 'email',
        ]


class Friends(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'idx',
            'sender_idx',
            'receiver_idx',
            'created_dt'
        ]


# track post 큰 카드 버젼
def get_likes_counts(obj):
    try:
        counts = Likes.objects.get_user_likes_count(obj.idx)
        return counts
    except:
        pass


class UserProfileDisplaySerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()  # user를 follow하는 users
    followings = serializers.SerializerMethodField()  # user가 follow 하는 users
    user_pic = serializers.SerializerMethodField()  # user profile avatar image
    profile_pic = serializers.SerializerMethodField()  # user profile 배경 이미지
    total_comment_counts = serializers.SerializerMethodField()  # user 가 댓글단 횟수
    likes_counts = serializers.SerializerMethodField()  # user 가 좋아요 누른 횟수

    class Meta:
        model = Users
        fields = [
            'objects',
            'idx',
            'user_id',
            'nickname',
            'email',
            'profile_pic',
            'background_pic',
            'follower_count',
            'following_count',
            'tracks_count',
            'grade',
            'status',
            'created_dt',
            'refresh_token',
            'followers',
            'followings',
        ]

    def get_profile_pic(self, obj):
        try:
            dic = json.loads(obj.profile)
            return dic["profile_pic"]
        except:
            pass

    def get_background_pic(self, obj):
        try:
            dic = json.loads(obj.profile)
            return dic["background_pic"]
        except:
            pass

    def get_total_comment_counts(self, obj):
        try:
            counts = Comments.objects.get_user_comment_counts(obj.idx)
            return counts

        except:
            pass
