from django.contrib.auth.models import User
from quickstart.models import Tweet, Follow
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'last_name', 'first_name']
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['url', 'id', 'text', 'photo', 'created', 'author']


class FollowSerializer(serializers.HyperlinkedModelSerializer):
    follows = UserSerializer(read_only=True)
    follower = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['follows', 'follower', 'followed']
#
#
# class UserFollowsSerializer(serializers.HyperlinkedModelSerializer):
#     follows = UserSerializer()
#
#     class Meta:
#         model = Follow
#         fields = ['follows', 'followed']
#
#
# class UserFollowedSerializer(serializers.HyperlinkedModelSerializer):
#     follower = UserSerializer()
#
#     class Meta:
#         model = Follow
#         fields = ['follower', 'followed']
