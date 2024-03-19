from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from home.models import CustomUser,UserProfile

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Posts(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'

    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (ARCHIVED, 'Archived'),
    ]

    title = models.CharField(max_length=200)
    subtitle1 = models.CharField(max_length=200)
    subtitle2 = models.CharField(max_length=200)
    subtitle3 = models.CharField(max_length=200)
    subtitle = models.TextField()
    intro = models.TextField()
    content1 = models.TextField()
    content2 = models.TextField()
    content3 = models.TextField()
    image = models.ImageField(upload_to='media/post_images', blank=True, null=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': CustomUser.EDITOR})
    total_views = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PostView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')




class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    comment_author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.comment_author} on {self.post} at {self.created_date}"


