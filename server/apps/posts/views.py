from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Vote
from .serializers import PostsSerializer
from rest_framework import viewsets, status
from rest_framework import permissions


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post', 'delete'])
    def vote(self, request, pk):
        user, value = request.user, request.data.get('value')

        if request.method == 'DELETE':
            vote = Vote.objects.filter(user=user, post=self.get_object()).first()
            if vote.user != user:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

            vote.delete()
            return Response(status=status.HTTP_200_OK)

        if value not in [Vote.LIKE, Vote.DISLIKE]:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        vote, is_created = Vote.objects.update_or_create(user=user, post=self.get_object(),
                                                      defaults={'value': value})

        return Response(status=status.HTTP_200_OK)



