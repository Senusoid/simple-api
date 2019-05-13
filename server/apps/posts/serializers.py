from rest_framework import serializers
from .models import Post
from apps.users.serializers import UserSerializer


class PostsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'text', 'user', 'votes_stats')

    def to_representation(self, instance):
        data = super(PostsSerializer, self).to_representation(instance)
        user = self.context['request'].user
        data['is_voted'] = instance.votes.filter(user=user).exists()


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text')


class VoteSerializer(serializers.Serializer):
    value = serializers.IntegerField(min_value=-1, max_value=1)
