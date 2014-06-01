from setuptools import setup


setup(name='picoweb',
      version='0.1',
      description="""A very lightweight, memory-efficient async web framework
for MicroPython.org and its asyncio_micro.""",
      url='https://github.com/pfalcon/picoweb',
      author='Paul Sokolovsky',
      author_email='pfalcon@users.sourceforge.net',
      license='MIT',
      py_modules=['picoweb'],
      install_requires=['micropython-asyncio_micro'])
