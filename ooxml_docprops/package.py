"""Representation of an OOXML based Package.
"""

from os.path import abspath
from zipfile import ZipFile
from zip_utils import zipdir
import config
import os
import shutil
import tempfile


class OOXMLPackage(object):
    def __init__(self, zipped_path, read_only=False):
        self.zipped_path = abspath(zipped_path)
        self._read_only = read_only

        self._unpacked = False
        self.remove_workdir = True

        if config.DEBUG:
            self.remove_workdir = False

    def __enter__(self):
        self.workdir = tempfile.mkdtemp(prefix='docxtemp')
        self.unpack()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self._read_only:
            self.pack()

    def unpack(self):
        """Unpack a zipped OOXML Package into a working directory.
        """
        if config.DEBUG:
            print "Unpacking to %s" % self.workdir
        with ZipFile(self.zipped_path, 'r') as z:
            z.extractall(self.workdir)
        self._unpacked = True

    def pack(self):
        """Pack an unpacked OOXML Package into a ZIP file again.

        First, create a temporary directory and zip up the contents of
        self.workdir into a new ZIP in that location.
        If that was successful, move the newly created ZIP to the
        location of the original input file, overwriting it.
        """

        temp_zip_location = tempfile.mkdtemp(prefix='docx_temp_zip')
        temp_zip_path = os.path.join(temp_zip_location, 'output.zip')
        if config.DEBUG:
            print "Packing to %s..." % temp_zip_path
        zipdir(self.workdir, temp_zip_path)
        if config.DEBUG:
            print "Moving to %s" % self.zipped_path
        shutil.move(temp_zip_path, self.zipped_path)
        shutil.rmtree(temp_zip_location)
        if self.remove_workdir:
            shutil.rmtree(self.workdir)
        self._unpacked = False
