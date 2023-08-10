from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

routerv1 = routers.DefaultRouter()
routerv1.register(r'posts', PostViewSet)
routerv1.register(
    r'posts/(?P<id>\d+)/comments', CommentViewSet, basename='comments',
)
routerv1.register(r'groups', GroupViewSet, basename='group')
routerv1.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(routerv1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
