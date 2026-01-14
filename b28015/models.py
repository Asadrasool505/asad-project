from django.db import models
from django.contrib.auth.models import User

# This creates the Blog table
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title # Admin mein Post ka Title dikhayega

# This creates the Comment table with an AI field
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    # This field will store the AI result (Positive/Negative)
    sentiment = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.text[:20]}... ({self.sentiment})" # Admin mein Sentiment dikhayega