from ua_mapper.wsgi import UAMapper

class MyMapper(UAMapper):
    def map(self, device):
        """
        Override this method to perform your own custom mapping.
        """
        if device.resolution_width < 240:
            return 'medium'
        else:
            return 'high'
    
application = MyMapper()
