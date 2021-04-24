from django.db import models


class Tweet(models.Model):
    text = models.CharField(max_length=1000)
    photo = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.author.username}] {self.text}'


class Follow(models.Model):
    # User(username=v1, follows=[v1->v2, v1->v3], followers=[v3->v1])
    follower = models.ForeignKey('auth.User', related_name='follows', on_delete=models.CASCADE)
    follows = models.ForeignKey('auth.User', related_name='followers', on_delete=models.CASCADE)
    followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.follower.username}] {self.follows}'
