import datetime, random
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.template.loader import get_template, render_to_string
from django.conf import settings

import settings as pq_settings

class QuoteManager(models.Manager):
    def add_quote(self, text, author=None, obj=None, sites=[]):
        content_type, object_id, author = None, None, author
        if obj:
            content_type = ContentType.objects.get_for_model(obj)
            object_id = obj.pk
            
        new = self.create(text=text, author=author, content_type=content_type,
            object_id=object_id)
        
        # If a list of sits is not specified, add the default site.
        if not sites:
            new.sites.add(Site.objects.get(pk=settings.SITE_ID))
        else:
            for site in sites:
                new.sites.add(site)
    
    def _get_random(self, num=None, content_type=None, count=0):
        kwargs = {'sites__in': [settings.SITE_ID,]}
        if content_type:
            kwargs["content_type__pk"] = content_type.pk
            
        if not isinstance(num, int):
            num = int(num)
            
        q = self.filter(**kwargs).order_by('-add_date')
        
        # If q is empty return None
        if not q:
            return None
        
        # If count a specified trim the list down
        if count:
            q = q[:count]
           
        ret = None
        # If num is greater than 1, return a random list
        if num and num > 1:
            if num > len(q):
                num = len(q)
            ret = random.sample(q, num)
        
        # Default will return one random item
        if not ret:
            ret = random.sample(q, 1)[0]
            
        return ret
        
    def random(self, content_type=None, count=0):
        return self._get_random(num=1, content_type=content_type, count=count)
        
    def random_list(self, num=5, content_type=None, count=0):
        return self._get_random(num=num, content_type=content_type, count=count)
    

class Quote(models.Model):
    text = models.TextField(_('Quote'))
    author = models.CharField(_('Author'), max_length=255, 
        null=True, blank=True)
    content_type = models.ForeignKey(ContentType, 
        verbose_name=_('Content Type'), null=True, blank=True)
    object_id = models.IntegerField(_('Object ID'), null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    add_date = models.DateTimeField(_('Date Added'), 
        default=datetime.datetime.now)
    sites = models.ManyToManyField(Site)
    
    objects = QuoteManager()
    
    class Meta:
        get_latest_by = "add_date"
    
    def __unicode__(self):
        return self.text
        
    def render(self, template=None):
        t, model, app = None, "", ""
        # build the cache key
        cache_key = "%s.%s.template" % (pq_settings.CACHE_PREFIX, self.pk)
        
        # If a cached version of this render is found, return it
        t = cache.get(cache_key)
        if t: return t
        
        if self.content_type:
            model = self.content_type.model.lower()
            app = self.content_type.app_label.lower()
        try:
            # Retreive the template passed in
            t = get_template(template)
        except:
            try:
                # Make a key based off of associated content object
                key = '%s.%s' % (app, model)
                # Retreive the template from the settings
                t = get_template(pq_settings.TEMPLATES.get(key, ""))
            except:
                try:
                    # Retrieve the template based of off the content object
                    t = get_template('pullquote/%s__%s.html' % (model, app))    
                except:
                    try:
                        # Last resort, get template default
                        t = get_template('pullquote/default.html')
                    except:
                        pass
                
        if not t: return None
            
        # The conext that will be passed to the rendered template.
        context = {'quote': self}
            
        if self.content_object:
            context['object'] = self.content_object
        # Render the template
        ret = render_to_string(t.name, context)
        
        # Set the cache
        cache.set(cache_key, ret, pq_settings.CACHE_TIMEOUT)
        
        return ret
        