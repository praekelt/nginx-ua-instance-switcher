class SimpleMapper(object):
    def map(self, device):
        if device.resolution_width < 240:
            return 'medium'
        else:
            return 'high'
