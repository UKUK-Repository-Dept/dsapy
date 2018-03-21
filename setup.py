from setuptools import setup

setup(name='dsapy',
      version='0.2',
      description='Python client for DSpace 5.X API',
      url='http://github.com/jrihak/dsapy',
      author='Jakub Řihák',
      license='MIT',
      packages=['dsapy', 'dsapy/requests', 'dsapy/utils'],
      install_requires=['requests'],
      zip_safe=False)
