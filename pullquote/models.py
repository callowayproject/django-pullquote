import datetime
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.cache import cache

class QuoteManager(models.Manager):
    def get_random(self, content_type=None, count=0):
        """
        Retrieve a random quote with optional arguments of
        content type and count.
        
        Count argument tells how many quotes to pick from sorted by date.
        """
        pass
    

class Quote(models.Model):
    text = models.TextField(_('Quote'))
    content_type = models.ForeignKey(ContentType, verbose_name=_('Content Type'))
    object_id = models.CharField(_('Object ID'), max_length=255)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    add_date = models.DateTimeField(_('Date Added'), default=datetime.datetime.now)
    sites = models.ManyToManyField(Site)
    
    def __unicode__(self):
        return self.quote
        
    