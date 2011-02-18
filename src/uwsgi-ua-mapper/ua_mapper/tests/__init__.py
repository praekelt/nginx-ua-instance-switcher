import unittest
import urllib2

from ua_mapper.management.commands import mapuseragents, wurfl

class NginxLookupTestCase(unittest.TestCase):

    def test_nginx_lookup(self):
        command = mapuseragents.Command()
        mapper = command.get_mapper()

        for i, ua in enumerate(wurfl.devices.uas):
            device = wurfl.devices.select_ua(ua)
            mapped_result = mapper.map(device)
            nginx_result = urllib2.urlopen(urllib2.Request("http://localhost", headers={'User-Agent' : ua})).read().split("\n")
            self.failUnless(mapped_result == nginx_result[0])
            self.failUnless(ua == nginx_result[1])
            print (nginx_result)
