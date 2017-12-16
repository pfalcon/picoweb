from setuptools import setup
import sdist_upip


setup(name='picoweb',
      version='1.3',
      description="A very lightweight, memory-efficient async web framework \
for MicroPython.org and its uasyncio module.",
      long_description="More documentation is available at https://github.com/pfalcon/picoweb",
      url='https://github.com/pfalcon/picoweb',
      author='Paul Sokolovsky',
      author_email='pfalcon@users.sourceforge.net',
      license='MIT',
      cmdclass={'sdist': sdist_upip.sdist},
      packages=['picoweb'],
      # Note: no explicit dependency on 'utemplate', if a specific app uses
      # templates, it must depend on it.
      install_requires=['micropython-uasyncio', 'micropython-pkg_resources'])
