from distutils.core import setup, Extension

foohid = Extension('foohid',
                   sources=['mouse_control.c'],
                   extra_link_args=['-framework', 'IOKit'])


setup(name='offkeyboard',
      version='1.0.0',
      description='send I/O events with an instrument',
      ext_modules=[foohid])
