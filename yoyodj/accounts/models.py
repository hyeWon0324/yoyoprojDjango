from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse_lazy
import datetime
# Create your models here.


class UserProfileManager(models.Manager):
    use_for_related_fields = True

    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = Users.objects.get_or_create(user=user) # (user_obj, true)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else:
            user_profile.following.add(to_toggle_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = Users.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False

    def recommended(self, user, limit_to=10):
        print(user)
        profile = user.profile 
        following = profile.following.all()
        following = profile.get_following()
        qs = self.get_queryset().exclude(user__in=following).exclude(id=profile.id).order_by("?")[:limit_to]
        return qs


class Users(models.Model):
    idx = models.AutoField(primary_key=True)
    user_id = models.CharField(unique=True, max_length=45)
    pw = models.CharField(max_length=80)
    nickname = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45)
    profile = models.CharField(max_length=500, blank=True, null=True)
    salt = models.CharField(max_length=64)
    follower_count = models.IntegerField(blank=True, null=True)
    following_count = models.IntegerField(blank=True, null=True)
    tracks_count = models.IntegerField(blank=True, null=True)
    grade = models.IntegerField()
    status = models.IntegerField()
    created_dt = models.DateTimeField(default=datetime.datetime.utcnow())
    access_dt = models.DateTimeField(blank=True, null=True)
    updated_dt = models.DateTimeField(blank=True, null=True)
    refresh_token = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return str(self.following_count)


class Friends(models.Model):
    idx = models.AutoField(primary_key=True)
    sender_idx = models.ForeignKey('Users', models.DO_NOTHING, db_column='sender_idx', related_name='fk_friends_1')
    receiver_idx = models.ForeignKey('Users', models.DO_NOTHING, db_column='receiver_idx', related_name='fk_friends_2')
    created_dt = models.DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        managed = False
        db_table = 'friends'

    def get_following(self):
        users = Friends.sender_idx.all()  # User.objects.all().exclude(username=self.user.username)
        return users.exclude(username=self.user.username)

    def get_follow_url(self):
        return reverse_lazy("profiles:follow", kwargs={"username": self.user.username})

    def get_absolute_url(self):
        return reverse_lazy("profiles:detail", kwargs={"username": self.user.username})


'''
class UserProfile(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile') # user.profile 
    following   = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by') 
    # user.profile.following -- users i follow
    # user.followed_by -- users that follow me -- reverse relationship

    objects = UserProfileManager() # UserProfile.objects.all()
    # abc = UserProfileManager() # UserProfile.abc.all()

    def __str__(self):
        return str(self.following.all().count())

    def get_following(self):
        users  = self.following.all() # User.objects.all().exclude(username=self.user.username)
        return users.exclude(username=self.user.username)

    def get_follow_url(self):
        return reverse_lazy("profiles:follow", kwargs={"username":self.user.username})

    def get_absolute_url(self):
        return reverse_lazy("profiles:detail", kwargs={"username":self.user.username})
'''

# cfe = User.objects.first()
# User.objects.get_or_create() # (user_obj, true/false)
# cfe.save()


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        new_profile = Users.objects.get_or_create(user=instance)
        # celery + redis
        # deferred task


post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)






