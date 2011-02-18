Django UA Mapper
================

A simple Django view mapping a User-Agent header strings to some value determined by a user defined module using Wurfl. The resulting value is stored in cache with the md5'd User-Agent header string as key.


Installation
------------
#. Install or add django-ua-mapper to your Python path.
#. Add ``ua_mapper`` to your ``INSTALLED_APPS`` setting in your project's ``settings.py`` file. 
#. Setup Django `caching <http://docs.djangoproject.com/en/dev/topics/cache/>`_. For Nginx lookups its recommended to use Memcached as cache backend.
#. Add a ``UA_MAPPER_CLASS`` setting to your project's ``settings.py`` file. This setting specifies the module to use for the actual mapping (see Mapper Class below), i.e.::

    UA_MAPPER_CLASS = 'project.uamappers.SimpleMapper'

#. Add the mapping urls to your project's ``urls.py`` file::
    
    (r'^mapper/', include('ua_mapper.urls')),

Now if you hit ``http://<host>/mapper/map-request/`` a mapping will be performed and its result stored in Cache with the md5'd requesting User-Agent header string as key.

Usage
-----

Update Wurfl Database
~~~~~~~~~~~~~~~~~~~~~

#. To update the Wurfl database run the ``updatewurfl`` command as follows::

    $ ./manage.py updatewurfl

#. The Wurfl database will only be updated when a new downloadable Wurfl database is found. To force an update run the command as follows::

    $ ./manage.py updatewurfl

Mapper Class
------------
The mapper class is a single Python class that defines the following method:

map
~~~

map(self, device)

``device`` is a Wurfl device object. This method is called for each device in the Wurfl database whenever ``mapuseragents`` is run. ``map()`` must return a string, which will be stored in Redis as the value for the md5'd User-Agent key. 

Example
~~~~~~~

This example mapper returns a simple category string for each device, based on the device's resolution::

    class SimpleMapper(object):
        def map(self, device):
            if device.resolution_width < 240:
                return 'medium'
            else:
                return 'high'

Examples
--------

An Nginx example is included showing how to use this mapper for efficient mapping with straight Memcached lookups from within Nginx. 

