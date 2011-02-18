import hashlib

from django.http import HttpResponse

from ua_mapper.mapper import UAMapper
from djanginxed.decorators.cache import cache_page

def key_generator(request):
    """
    Custom cache key generator to generate a key from requesting User Agent.
    """
    return hashlib.md5(request.META['HTTP_USER_AGENT']).hexdigest()

@cache_page(60 * 15, key_generator=key_generator)
def map_request(request):
    mapper = UAMapper()
    user_agent, device, value = mapper.map_by_request(request)
    return HttpResponse(value)
