from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from pywurfl.algorithms import TwoStepAnalysis

class UAMapper(object):
    def get_mapper(self):
        try:
            mapper_path = settings.UA_MAPPER_CLASS
        except:
            raise ImproperlyConfigured('No UA_MAPPER_CLASS setting found.')
        try:
            dot = mapper_path.rindex('.')
        except ValueError:
            raise ImproperlyConfigured('%s isn\'t a UA Mapper module.' % mapper_path)
        module, classname = mapper_path[:dot], mapper_path[dot+1:]    
        try:
                mod = import_module(module)
        except ImportError, e:
            raise ImproperlyConfigured('Could not import UA Mapper %s: "%s".' % (module, e))    
        try:
            mapper_class = getattr(mod, classname)
        except AttributeError:
            raise ImproperlyConfigured('UA mapper module "%s" does not define a "%s" class.' % (module, classname))
   
        mapper_instance = mapper_class()
        if not hasattr(mapper_instance, 'map'):
            raise ImproperlyConfigured('UA mapper class "%s" does not define a map method. Implement the method to receive a Wurfl device object and return an appropriate value to be stored in Redis.' % classname)
        
        if not hasattr(mapper_instance, 'map'):
            raise ImproperlyConfigured('UA mapper class "%s" does not define a map method.' % classname)
        
        return mapper_class()
    
    def map(self, user_agent, device):
        mapper = self.get_mapper()
        value = mapper.map(device)
        return user_agent, device, value

    def map_by_request(self, request):
        from ua_mapper.management.commands import wurfl
        user_agent = unicode(request.META.get('HTTP_USER_AGENT', ''))
        if user_agent:
            devices = wurfl.devices
            search_algorithm = TwoStepAnalysis(devices)
            device = devices.select_ua(user_agent, search=search_algorithm)
            return self.map(user_agent, device)
