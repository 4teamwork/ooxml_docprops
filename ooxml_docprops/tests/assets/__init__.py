from os.path import abspath
from os.path import dirname
from os.path import join
from tempfile import NamedTemporaryFile
import os


def path_to(asset_filename):
    return join(dirname(abspath(__file__)), asset_filename)


def as_tempfile(asset_filename):
    asset = open(path_to(asset_filename), 'rb')

    with NamedTemporaryFile(delete=False) as tmpfile:
        tmpfile.write(asset.read())
        return tmpfile


class TestAsset(object):
    """Creates and wraps temporary assets that can be used for a test-case."""

    def __init__(self, filename):
        self.filename = filename
        self.tmpfile = None

    @property
    def path(self):
        if not self.tmpfile:
            return None

        return self.tmpfile.name

    def __enter__(self):
        asset = open(path_to(self.filename), 'rb')

        with NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(asset.read())
        self.tmpfile = tmpfile
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.remove(self.tmpfile.name)
