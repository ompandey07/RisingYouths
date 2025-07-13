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
    


class GalleryCategory(models.TextChoices):
    EVENTS = 'Events', 'Events'
    MEETINGS = 'Meetings', 'Meetings'
    FESTIVALS = 'Festivals', 'Festivals'
    SUCCESS_STORIES = 'Success Stories', 'Success Stories'
    TRAININGS = 'Trainings', 'Trainings'
    COMMUNITY_WORK = 'Community Work', 'Community Work'
    OTHERS = 'Others', 'Others'

class ManpowerGallery(models.Model):
    category = models.CharField(
        max_length=50,
        choices=GalleryCategory.choices,
        default=GalleryCategory.OTHERS
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    gallery_image = models.ImageField(upload_to='Gallery_images/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.category} - {self.created_at.strftime('%Y-%m-%d')}"




class YouthJob(models.Model):
    CATEGORY_CHOICES = [
        ('unskilled', 'Unskilled'),
        ('semiskilled', 'Semi-skilled'),
        ('skilled', 'Skilled'),
        ('professional', 'Professional'),
    ]

    job_title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    job_image = models.ImageField(upload_to='Job_Images/')
    job_description = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job_title