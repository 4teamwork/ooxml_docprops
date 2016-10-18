import os
from setuptools import setup, find_packages


version = '1.3.0'


tests_require = [
    'unittest2',
    ]


setup(name='ooxml_docprops',
      version=version,
      description='Populates OOXML documents with custom DocProperties',

      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      classifiers=[
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ooxml docx metadata docprops docproperties properties',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ooxml_docprops',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'iso8601',
        'lxml',
        'setuptools',
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points='''
      # -*- Entry points: -*-
      [console_scripts]
      update-properties = ooxml_docprops.cli:update_props
      read-properties = ooxml_docprops.cli:read_props
      ''',
      )
