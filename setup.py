#!/usr/bin/env python
from setuptools import setup
#from distutils.core import setup
import warnings
import subprocess

try:
   rst = subprocess.check_output("pandoc README.md -w rst".split())
except:
   warnings.warn("Could not convert markdown readme to RST")
   rst = ""
   raise
setup(name='Localize_M',
      version='1.0.1',
      description='Localize objc M files',
      long_description=open("README.rst").read(),
      author='Jacco Taal',
      author_email='jacco@bitnomica.com',
      url='https://github.com/jrtaal/localize_m',
      license="LICENSE.txt",
      packages=['localize_m'],
      classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
      ],
      install_requires = [ 
       "colored",
       "slugify", 
       "gnureadline",
      ] ,
      entry_points = {
        'console_scripts' : ['localize_m = localize_m.main:main' ]
      }
     )
