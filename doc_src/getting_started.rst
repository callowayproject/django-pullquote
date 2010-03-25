.. _getting started:

Getting Started
===============

:doc:`Download and Install <installation>` the PullQuote app.


Creating your first quote
*************************

.. code-block:: python

    from pullquote.models import Quote
    
    Quote.objects.add_quote(text="This is my quote")
    
    
Only required argument is `text`, but for more functionality you can also provide a content object from where this quote was found.

.. code-block:: python
    
    from blog.models import Entry

    entry = Entry.objects.get(...)

    Quote.objects.add_quote(text="I will live forever", object=entry)


Learn more about the models :doc:`here <reference/models>`


This will relate your `Quote` to a content objects and thus can be linked to its detail page. For example,
if you want to display who wrote the quote and it is linked to a Entry object as above, you can display the
author's name for the Entry.


Retrieving Quotes
*****************

You can retrieve Quotes by any means you see fit. This app includes some simple fetch method.


random
^^^^^^

.. code-block:: python

    quote = Quote.objects.random()
    
    
.. note::
    
    This method will return 1 random object. You can specify 2 optional arguments, `content_type`, which will return only that content_type and `count` which will only grab a random quote from a shorten number of Quotes. This list is ordered by the `add_date` so the latest Quote is first.
    
    
random_list
^^^^^^^^^^^

.. code-block:: python

    quote = Quote.objects.random_list(num=N)
    
    
.. note::

    Same as above, but will return a list of the `num` specified. This also has the same extra arguments of `content_type` and `count`.
    
    
Retrieving your Quotes via template tags
****************************************

There are three template tags included that you can use to retrieve your Quotes


Getting the latest Quote
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

    {% pullquote_latest as latest_quote %}
    
This template tag simply returns the latest quote by the add date. Takes in one optional argument `content_type`

.. code-block:: django

    {% pullquote_latest as latest_quote with content_type=blog.entry %}
    
This will only return the latest `Quote` that has the specified content type associated with it.


Getting random Quote
^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

    {% pullquote_random as object %}
    
This template tag just returns a random `Quote` object and assigns it to the `object` variable. Similar to the manager method it can take two optional arguments


.. code-block:: django

    {% pullquote_random as object with content_type=blog.entry %}
    
or

.. code-block:: django
    
    {% pullquote_random as object with content_type=blog.entry count=25 %}
    
or

.. code-block:: django

    {% pullquote_random as object with count=25 %}
    
    
Getting a list of random Quotes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

    {% pullquote_random_list 5 as object_list %}
    
Same as above but will return a list of quotes and assigns it to `object_list` variable. And same as above you can specify two optional arguments

.. code-block:: django

    {% pullquote_random_list 5 as object_list with content_type=blog.entry %}

or

.. code-block:: django    
    
    {% pullquote_random_list 5 as object_list with content_type=blog.entry count=25 %}
    
or

.. code-block:: django

    {% pullquote_random_list 5 as object_list with count=25 %}
    
    
Render your quotes
******************

You can use the `Quote` object just to display the `text` attribute or you can use the `render` method to render the `Quote` by it's associated content object.

.. code-block:: django

    {% pullquote_random as quote %}
    
    {{ quote.render }}
    
Default template used to render a Quote is pullquote/default.html.

You can create content type specific templates to render quotes, if a content object was providing when creating the `Quote`

* pullquote/app__model.html
* pullquote/blog__entry.html


You can also specify the different templates in the settings

.. code-block:: python

    PULLQUOTE_TEMPLATES = {
        "blog.entry": "blog/quotes/entry.html",
        "blog.blog": "pullquote/blog.html",
    }
    
.. note::
    
    More information about the settings :doc:`here <reference/settings>`. 


Render Template Tag
^^^^^^^^^^^^^^^^^^^

You can also use this render template tag as well.

.. code-block:: django

    {% pullquote_render quote %}
    
Witch is the same as 

.. code-block:: django

    {% pullquote_random as quote %}
    
    {{ quote.render }}
    
There is one additional argument `template` you can specify to render a custom template

.. code-block:: django

    {% pullquote_render quote with template=pullquote/custom.html %}
    
    
    
Template render order
^^^^^^^^^^^^^^^^^^^^^

* If you are using the `pullquote_render` template tag, and specify a template, that template will be checked first
* If no template is specified in the `pullquote_render` template tag
    #. `PULLQUOTE_TEMPLATES` setting is checked for associated templates
    #. Model specific templates are then checked
    #. Default template is used


