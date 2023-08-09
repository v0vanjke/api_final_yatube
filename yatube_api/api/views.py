from rest_framework import filters, mixins, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAuthorOrReadOnlyPermission
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Comment, Group, Post, User

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def perform_create(self, serializer):
        serializer.save(
            post_id=self.kwargs.get('id'),
            author=self.request.user,
        )

    def get_queryset(self):
        comment_queryset = Comment.objects.filter(post=self.kwargs.get('id'))
        return comment_queryset


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CreateRetrieveListMixin(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet,
):
    """Make your own BaseClass."""

    pass


class FollowViewSet(CreateRetrieveListMixin):
    """Deal with Create and Post requests."""

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        """Validate situation when User = Follower."""
        following = User.objects.get(
            username=self.request.data.get('following')
        )
        user = self.request.user
        if user == following:
            raise ValidationError('Нельзя подписываться самому на себя!')
        serializer.save(user=user, following=following)

    def get_queryset(self):
        """Return queryset with all followers."""
        return self.request.user.following.all()
