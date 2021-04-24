from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet
from quickstart.models import Tweet, Follow
from rest_framework import viewsets, mixins

from quickstart.permissions import IsTweetAuthorOrReadOnly
from quickstart.serializers import UserSerializer, TweetSerializer, FollowSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    lookup_field = 'username'


class TweetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tweet to be viewed or edited.
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [
        IsTweetAuthorOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserTweetsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tweet.objects
    serializer_class = TweetSerializer

    def get_queryset(self):
        return self.queryset.filter(
            author__username=self.kwargs['parent_lookup_username']
        )


class FollowViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    queryset = Follow.objects
    serializer_class = FollowSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    def perform_create(self, serializer):
        follows = User.objects.get(username=self.kwargs[self.lookup_field])
        serializer.save(
            follower=self.request.user,
            follows=follows
        )

    def get_object(self):
        return self.queryset.filter(
            follower=self.request.user,
            follows__username=self.kwargs[self.lookup_field]
        )


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tweet.objects.order_by('-id')
    serializer_class = TweetSerializer

    def get_queryset(self):
        return (self.queryset.filter(
            author__followers__follower=self.request.user
        ) | self.queryset.filter(author=self.request.user))


class UserFollowsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Follow.objects
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.queryset.filter(
            follower__username=self.kwargs['parent_lookup_username'])


class UserFollowedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Follow.objects
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.queryset.filter(
            follows__username=self.kwargs['parent_lookup_username'])
