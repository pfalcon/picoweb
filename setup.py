from setuptools import setup


setup(name='picoweb',
      version='1.0',
      description="""A very lightweight, memory-efficient async web framework
for MicroPython.org and its uasyncio module.""",
      url='https://github.com/pfalcon/picoweb',
      author='Paul Sokolovsky',
      author_email='pfalcon@users.sourceforge.net',
      license='MIT',
      packages=['picoweb'],
      # Note: no explicit dependency on 'utemplate', if a specific app uses
      # templates, it must depend on it.
      install_requires=['micropython-uasyncio'])
