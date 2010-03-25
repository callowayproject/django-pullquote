from django.template import Library, Node, TemplateSyntaxError, Variable, resolve_variable, VariableDoesNotExist
from django.contrib.contenttypes.models import ContentType
from pullquote.models import Quote
register = Library()

class LatestNode(Node):
    def __init__(self, varname, **kwargs):
        self.varname, self.kwargs = varname, kwargs
        
    def render(self, context):
        context[self.varname] = None
        try:
            context[self.varname] = Quote.objects.filter(**self.kwargs).latest()
        except:
            pass
        return ""
        

class RandomNode(Node):
    def __init__(self, varname, num=1, **kwargs):
        self.num, self.varname, self.kwargs = num, varname, kwargs
        
    def render(self, context):
        if self.num == 1:
            ret = Quote.objects.random(**self.kwargs)
        else:
            ret = Quote.objects.random_list(self.num, **self.kwargs)
        context[self.varname] = ret
        return ""
        
        
def do_pullquote_latest(parser, token):
    argv = token.contents.split()
    argc = len(argv)

    if argc != 3 and argc != 5:
        raise TemplateSyntaxError, "Tag %s takes two or four arguments." % argv[0]

    if argv[1] != "as":
        raise TemplateSyntaxError, "First argument must be 'as' for tag %s" % argv[0]
            
    kwargs = {}
    if argc == 5:
        if argv[3] != "with":
            raise TemplateSyntaxError, "Thrid argument must be 'with' for tag %s" % argv[0]
            
        extra = argv[4].split("=")
        if len(extra) != 2 and extra[0] != "content_type":
            raise TemplateSyntaxError, "Fourth argument must be 'content_type=[model.app]' for tag %s" % argv[0]
            
        try:
            ctype = ContentType.objects.get(
                app_label=extra[1].split(".")[0],
                model=extra[1].split(".")[1])
        except:
            raise TemplateSynaxError, "Fourth argument value for 'content_type' was not a valid 'ContentType` object for tag %s" % argv[0]
        kwargs["content_type"] = ctype
    return LatestNode(argv[2], **kwargs)
    
def do_pullquote_random(parser, token):
    argv = token.contents.split()
    argc = len(argv)
    
    if not argc in range(3, 7):
        raise TemplateSyntaxError, "Tag %s takes three, five or six arguments." % argv[0]
        
    if argv[1] != "as":
        raise TemplateSyntaxError, "First argument must be 'as' for tag %s" % argv[0]
        
    kwargs = {}
    if argc > 3:
        if argv[3] != "with":
            raise TemplateSyntaxError, "Third argument must be 'with' for tag %s" % argv[0]
        
        for argument in argv[4:]:
            extra = argument.split("=")
            if len(extra) != 2:
                raise TemplateSyntaxError, "One or more extra arguments for tag %s are not formatted correctly." % argv[0]
            if not extra[0] in ["content_type", "count"]:
                raise TemplateSyntaxError, "Only 'content_type and/or 'count' are valid extra arguments for tag %s" % argv[0]
            
            if extra[0] == "content_type":
                try:
                    ctype = ContentType.objects.get(
                        app_label=extra[1].split(".")[0],
                        model=extra[1].split(".")[1])
                    kwargs["content_type"] = ctype
                except:
                    raise TemplateSyntaxError, "Value for 'content_type' extra argument was not a valid 'ContentType` object for tag %s" % argv[0]
            else:
                kwargs["count"] = int(extra[1])
    return RandomNode(argv[2], num=1, **kwargs)
    
def do_pullquote_random_list(parser, token):
    
    argv = token.contents.split()
    argc = len(argv)
    
    if not argc in range(4, 8):
        raise TemplateSyntaxError, "Tag %s takes three, five or six arguments." % argv[0]
        
    if argv[2] != "as":
        raise TemplateSyntaxError, "Second argument must be 'as' for tag %s" % argv[0]

    kwargs = {}  
    if argc > 4:
        if argv[4] != "with":
            raise TemplateSyntaxError, "Fourth argument must be 'with' for tag %s" % argv[0]
            
        for argument in argv[5:]:
            extra = argument.split("=")
            if len(extra) != 2:
                raise TemplateSyntaxError, "One or more extra arguments for tag %s are not formatted correctly." % argv[0]
            if not extra[0] in ["content_type", "count"]:
                raise TemplateSyntaxError, "Only 'content_type and/or 'count' are valid extra arguments for tag %s" % argv[0]
            
            if extra[0] == "content_type":
                try:
                    ctype = ContentType.objects.get(
                        app_label=extra[1].split(".")[0],
                        model=extra[1].split(".")[1])
                    kwargs["content_type"] = ctype
                except:
                    raise TemplateSynaxError, "Value for 'content_type' extra argument was not a valid 'ContentType` object for tag %s" % argv[0]
            else:
                kwargs["count"] = int(extra[1])
        
    return RandomNode(argv[3], argv[1], **kwargs)
            
            
def pullquote_render(quote, template=None):
    if isinstance(quote, Quote):
        return quote.render(template=template)
    
            
register.tag("pullquote_latest", do_pullquote_latest)
register.tag("pullquote_random", do_pullquote_random)
register.tag("pullquote_random_list", do_pullquote_random_list)
register.simple_tag(pullquote_render)