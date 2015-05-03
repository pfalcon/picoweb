from setuptools import setup


setup(name='picoweb',
      version='0.7.2',
      description="""A very lightweight, memory-efficient async web framework
for MicroPython.org and its uasyncio module.""",
      url='https://github.com/pfalcon/picoweb',
      author='Paul Sokolovsky',
      author_email='pfalcon@users.sourceforge.net',
      license='MIT',
      packages=['picoweb'],
      install_requires=['micropython-uasyncio', 'micropython-errno', 'micropython-time', 'utemplate'])
