from django.db import models
from django.utils import timezone 
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    text = models.TextField()
    create_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank = True, null = True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comments = True)

    def get_absolute_url(self):
        return reverse("blog_app:post_detail", kwargs = {'pk' : self.pk })    

    def __str__(self):  
        return self.title       


class Comment(models.Model):
    post = models.ForeignKey('blog_app.Post' , related_name = 'comments', on_delete = models.CASCADE)
    author = models.CharField(max_length = 255)
    text = models.TextField()
    create_date = models.DateTimeField(default = timezone.now)
    approved_comments = models.BooleanField(default = False)

    def approve(self):
        self.approved_comments = True
        self.save()
    
    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text    