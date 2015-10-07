#!/usr/bin/env python

from distutils.core import setup

setup(name='Localize_M',
      version='1.0',
      description='Localize objc M files',
      author='Greg Ward',
      author_email='jacco@bitnomica.com',
      url='https://gitlab.bitnomica.com/localize_m',
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
