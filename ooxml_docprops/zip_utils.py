"""Utility functions for dealing with ZIP files.
"""

from os.path import relpath
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
import os


def zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    with ZipFile(archivename, "w", ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                absolute_path = os.path.join(root, fn)
                relative_path = relpath(absolute_path, basedir)
                z.write(absolute_path, relative_path)
