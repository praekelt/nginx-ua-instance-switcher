Nginx User Agent Based Instance Switcher
========================================

With the wide range of modern web capable devices and the move towards the mobile web it has become crucially important to deliver content tailored for the requesting device's capabilities. It's no longer acceptable for high-end touch devices to simply render the desktop version of a website. At the opposite end low-end devices should not have to struggle loading content beyond its capabilities.

This is an example implimentation illustrating how you could harness Nginx, Wurfl, Memcached and a uWSGI process to deliver device specific web implementations. These implementations range from low to mid to high-end mobile, to conventional desktop, to full touch as required. Each implementation is nonetheless accessed using the same domain name.

Overview
--------

.. image:: https://github.com/downloads/praekelt/nginx-ua-instance-switcher/switcher.png

You can think of this whole process as load balancing but instead of round robin for instance the requesting device's capabilities determines which instance the request is forwarded to. Specifically, a device class is computed utilising Wurfl within a WSGI process. Once a device class is determined it is stored in Memcached using the requesting user-agent as key for future lookups. Nginx then simply forwards the request to a device class appropriate instance using the ``proxy_pass`` and ``upstream`` directives.

This approach is very fast since Memcached should over time contain all potential requesting user-agents, thus negating the need for slow Wurfl lookups. Also since the request is forwarded to an arbitrary upstream process this solution can be used with a variety of implementations, i.e. Django, Rails, PHP etc. For instance you can very happily implement a touch instance in Django and a desktop instance in Rails and run each without any knowledge of the other.

Configuration Specifics
-----------------------
In order for any of this to work you need a custom compiled version of Nginx that includes the following 3rd party modules:

    `Upstream Keepalive <http://wiki.nginx.org/HttpUpstreamKeepaliveModule>`_ – Provides keep-alive connections to Memcached upstreams.
    `Lua <http://github.com/chaoslawful/lua-nginx-module>`_ – Embed the power of Lua into Nginx.
    `Set Hash <https://github.com/simpl/ngx_http_set_hash>`_ – Set a variable to a variety of hash functions (upper/lowercase), including MD5.
    `uWSGI <http://wiki.nginx.org/HttpUwsgiModule>`_ – Allows Nginx to interact with uWSGI processes.

You can find an Ubuntu 10.04 PPA containing this custom Nginx `here <https://launchpad.net/~praekelt/+archive/nginx>`_.

As a simple example lets say you are running two web application instances, one for high-res/desktop devices and another for low-res/mobile devices. Example Nginx configuration is as follows::

    # Mobile upstream.
    upstream mobile {
        server 127.0.0.1:81;
    }

    # Desktop upstream.
    upstream desktop {
        server 127.0.0.1:82;
    }

    # Memcached upstream used to store device upstream values.
    upstream memcached {
        server 127.0.0.1:8001;
        keepalive 1024 single;
    }

    server {
        listen 80;
        server_name localhost;
    
        # Lookup upstream in uWSGI.
        location /map-request/dynamic/ {
            include uwsgi_params;
            uwsgi_param MEMCACHED_SOCKET 127.0.0.1:8001;
            uwsgi_pass 127.0.0.1:9002;
        }
    
        # Lookup upstream in Memcached.
        location /map-request/cached/ {
            set_md5 $memcached_key $http_user_agent;
            memcached_pass memcached;
        }
    
        # Pass request to user-agent appropriate upstream.
        location / {
            # Lookup device upstream.
            set $upstream "";
            access_by_lua '
                local result = ngx.location.capture("/map-request/cached/")
                if result.status == 200 then
                    ngx.var.upstream = result.body
                else
                    local result = ngx.location.capture("/map-request/dynamic/")
                    ngx.var.upstream = result.body
                end
                ngx.exit(ngx.OK)
            ';
            proxy_pass  http://$upstream;
            proxy_set_header Host $http_host;
        }
    }

The upstream sections defines two separate upstream processes, one for mobile and one for desktop. These can be configure however you see fit, Nginx will simply forward the request to one of these based on the requesting device's capabilities. For example the mobile upstream might be Django running behind Apache and the desktop upstream might be Rails running behind Nginx. A third upstream is defined pointing to a Memcached process used for storing hashed user-agent:category key value pairs to speed up lookups.

The server section defines three locations. The first, ``/map-request/dynamic/``, points to a uWSGI process that returns a string to be used as upstream for the requesting device. In this case either ``mobile`` or ``desktop``. The actual WSGI application is defined as follows::

    from ua_mapper.wsgi import UAMapper
    
    class MyMapper(UAMapper):
        def map(self, device):
            if device.resolution_width < 500:
                return 'mobile'
            else:
                return 'desktop'
    
    application = MyMapper()

This uses the `wsgi-ua-mapper(ua_mapper) <http://pypi.python.org/pypi/wsgi-ua-mapper>`_ Python library to simplify interfacing with Wurfl and Memcached. I don't want to go into too much detail, but essentially the UAMapper class takes care of resolving a Wurfl device for the incoming request and storing the map method’s result in Memcached. The only thing we have to do is implement a map method to return a string matching one of the upstreams defined in the Nginx configuration. In this case if a device has a resolution width larger than 500, we naively assume it's a desktop device and ``desktop`` is returned. Otherwise ``mobile`` is returned. Note that the map method is passed the requesting Wurfl device object. Thus you can use any of the requesting device`s attributes to determine a resulting upstream string.

The second location, ``/map-request/cached/``, points to a Memcached process. The WSGI process mentioned above stores mapped results in this Memcached process for faster future lookups.

The third location, ``/``, ties everything together. It uses Lua for some logic. Firstly the ``$upstream`` variable is set to an empty string. Then an upstream result is looked up from the ``/map-request/cached/`` (Memcached) location. If no result is found in Memcached, an upstream result is looked up from the ``/map-request/dynamic/`` (WSGI) location. Once an upstream has been determined the request is forwarded to it by the ``proxy_pass http://$upstream;`` directive.

So as an example lets say I access localhost using Firefox on my desktop computer. Lua tries to lookup an upstream for the requesting user-agent from Memcached. Lets say this is the first request to localhost from Firefox. At this stage Memcached will not yet have an upstream defined for the Firefox user-agent and will thus return a 404 status code. Lua then tries to lookup an upstream using the uWSGI process. Since Wurfl determines Firefox to have a resolution width larger than 500 pixels the WSGI app will return ``desktop`` as response body, as well as storing ``desktop`` in Memcached (using the md5 hashed user-agent string as key). The ``$upstream`` variable's value is now set as desktop in Nginx and the request is forwarded to the desktop usptream process defined as ``127.0.0.1:82``. On subsequent requests Memcached should contain a value for the Firefox user-agent string as stored by the WSGI app and hence the uWSGI location will not be accessed.

You can reference the Buildout contained here as a compete example.

