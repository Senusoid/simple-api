from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Vote
from .serializers import PostsSerializer, VoteSerializer, PostCreateSerializer
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    create_serializer_class = PostCreateSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'create':
            return self.create_serializer_class

        return self.serializer_class

    @swagger_auto_schema(
        methods=['post', 'delete'],
        operation_description='like/dislike/unlike',
        request_body=VoteSerializer
    )
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



