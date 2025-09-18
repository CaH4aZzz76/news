from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating_sum = sum(post.rating for post in self.posts.all())
        comment_rating_sum = sum(comment.rating for comment in self.user.comment_set.all())
        post_comments_rating = 0
        for post in self.posts.all():
            post_comments_rating += sum(comment.rating for comment in post.comment_set.all())
        self.rating = post_rating_sum * 3 + comment_rating_sum + post_comments_rating
        self.save()

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique= True)

class Post(models.Model):
    ARTICLE = 'ART'
    NEWS = 'NEW'
    POST_TYPE_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=3, choices=POST_TYPE_CHOICES)
    categories = models.ManyToManyField(Category, through='PostCategory')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
