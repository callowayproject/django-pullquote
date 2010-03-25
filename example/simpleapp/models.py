import datetime
from django.db import models

ARTICLE_CATEGORIES = (
    (0, "None"),
    (1, "News"),
    (2, "Opinion"),
    (3, "Sports"),
)

class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.IntegerField(choices=ARTICLE_CATEGORIES, default=0)
    author = models.CharField(max_length=255)
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return self.title