from django.db import models
from django.conf import settings
from django.db.models import Count, Q


class Post(models.Model):
    class Meta:
        db_table = 'posts'

    title = models.CharField(max_length=256)
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    @property
    def votes_stats(self):
        return self.votes.aggregate(like=Count('id', filter=Q(value=Vote.LIKE)),
                                    dislike=Count('id', filter=Q(value=Vote.DISLIKE)))

class Vote(models.Model):
    class Meta:
        db_table = 'votes'
        unique_together = ('user', 'post')


    LIKE = 1
    DISLIKE = -1
    VALUE_CHOICES = (
        (LIKE, 'LIKE'),
        (DISLIKE, 'DISLIKE'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='votes', on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VALUE_CHOICES)
