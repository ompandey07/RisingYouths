from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('TECH', 'Tech'),
        ('NEW', 'New'),
        ('INTERESTING', 'Interesting'),
        ('BREAKING', 'Breaking'),
        ('UPDATES', 'Updates'),
        ('NEWS', 'News'),
        ('ARTICLE', 'Article'),
        ('ACHIEVEMENTS', 'Achievements'),
        ('OTHERS', 'Others'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author.username}"