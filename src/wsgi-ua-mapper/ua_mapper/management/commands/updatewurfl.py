import os
import sys
from optparse import OptionParser
from urllib import urlopen

from django.core.management.base import BaseCommand
        
from wurfl2python import WurflPythonWriter, DeviceSerializer

OUTPUT_PATH = os.path.abspath(os.path.dirname(__file__))
WURFL_ARCHIVE_PATH = os.path.join(OUTPUT_PATH, "wurfl.zip")
WURFL_XML_PATH = os.path.join(OUTPUT_PATH, "wurfl.xml")
WURFL_PY_PATH = os.path.join(OUTPUT_PATH, "wurfl.py")

WURFL_DOWNLOAD_URL = 'http://downloads.sourceforge.net/project/wurfl/WURFL/latest/wurfl-latest.zip'

class Command(BaseCommand):
    help = 'Updates Wurfl devices database.'

    def write_archive(self, filename, data):
        f = open(WURFL_ARCHIVE_PATH, "w")
        f.write(data)
        f.close()

    def fetch_latest_wurfl(self):
        print "Downloading Wurfl..."
        data = urlopen(WURFL_DOWNLOAD_URL).read()
        self.write_archive(WURFL_ARCHIVE_PATH, data)
        os.system("unzip -o %s -d %s" % (WURFL_ARCHIVE_PATH, OUTPUT_PATH)) 
        return True
        
    def wurfl_to_python(self):
        print "Compiling device list..."
        
        # Setup options.
        op = OptionParser()
        op.add_option("-l", "--logfile", dest="logfile", default=sys.stderr,
              help="where to write log messages")
       
        # Cleanup args for converter to play nicely.
        if '-f' in sys.argv:
            sys.argv.remove('-f')
        if '--force' in sys.argv:
            sys.argv.remove('--force')
        
        options, args = op.parse_args()
        options = options.__dict__
        options.update({"outfile": WURFL_PY_PATH})

        # Perform conversion.
        wurfl = WurflPythonWriter(WURFL_XML_PATH, device_handler=DeviceSerializer, options=options)
        wurfl.process()

    def handle(self, *args, **options):
        self.fetch_latest_wurfl()
        self.wurfl_to_python()
        from wurfl import devices
        print "Done."
