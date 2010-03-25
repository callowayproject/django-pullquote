.. _download and install:

Installation
============



* Get the PullQuote App from `here <http://opensource.washingtontimes.com/projects/pullquote>`_
* Put the project somewhere on your python path.
* Add `pullquote` to your insalled_apps setting::

    INSTALLED_APPS = [
        ...
        pullquote,
        ...
    ]

* Sync the database::

    ./manage.py syncdb

