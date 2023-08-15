from setuptools import setup

import codecs
import os

major = 1
minor = 0
patch = 0

version = f"{major}.{minor}.{patch}"

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
  name = 'nysdotapi',
  version = version,
  license = 'MIT',
  description = 'NYS DOT Traffic Camera Python API',
  long_description_content_type = "text/markdown",
  long_description = long_description,
  author = 'Ryan Rudes',
  author_email = 'ryanrudes@gmail.com',
  url = 'https://github.com/ryanrudes/traffic',
  keywords = ['ny', 'traffic', 'live', 'stream', 'feed', 'camera', 'road', 'street'],
  packages = ['traffic'],
  install_requires = ['pillow', 'numpy', 'opencv-python'],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'Natural Language :: English',
    'Topic :: Database',
    'Topic :: Multimedia :: Video',
    'Topic :: Scientific/Engineering :: Image Processing',
    'Topic :: Scientific/Engineering :: Image Recognition',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
  ],
)