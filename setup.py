from distutils.core import setup, Extension

foohid = Extension('foohid',
                   sources=['foohid.c'],
                   extra_link_args=['-framework', 'IOKit'])


setup(name='offkeyboard',
      version = '0.2',
      description='send I/O events with an instrument',
      ext_modules=[foohid])
