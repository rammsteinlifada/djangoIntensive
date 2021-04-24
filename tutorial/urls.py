from django.urls import include, path
from quickstart import views
from quickstart.router import SwitchDetailRouter
from rest_framework_extensions.routers import ExtendedDefaultRouter
from django.contrib import admin
from quickstart.views import UserTweetsViewSet, UserFollowsViewSet, UserFollowedViewSet

switch_router = SwitchDetailRouter()

router = ExtendedDefaultRouter()
router.register(r'users', views.UserViewSet)
switch_router.register(r'follow', views.FollowViewSet)
router.register(r'users', views.UserViewSet).register(
    'tweets', UserTweetsViewSet, 'user-tweets', ['username'])
router.register(r'users', views.UserViewSet).register(
    'follows', UserFollowsViewSet, 'user-follows', ['username'])
router.register(r'users', views.UserViewSet).register(
    'followed', UserFollowedViewSet, 'user-followed', ['username'])
router.register(r'tweets', views.TweetViewSet)
router.register(r'feed', views.FeedViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('v1/', include(switch_router.urls)),
    path('v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
