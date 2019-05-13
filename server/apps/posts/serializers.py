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

        return data

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'text')

    def create(self, validated_data):
        user = self.context['request'].user
        post = Post.objects.create(user=user, **validated_data)
        return post


class VoteSerializer(serializers.Serializer):
    value = serializers.IntegerField(min_value=-1, max_value=1)
