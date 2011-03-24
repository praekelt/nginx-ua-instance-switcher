from ua_mapper.wsgi import UAMapper

class MyMapper(UAMapper):
    def map(self, device):
        if device.resolution_width < 500:
            return 'mobile'
        else:
            return 'desktop'
    
application = MyMapper()
