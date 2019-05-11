from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Vote
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

