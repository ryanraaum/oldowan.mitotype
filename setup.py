from setuptools import setup, find_packages
import sys, os

PACKAGE = 'mitotype'

VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'oldowan', PACKAGE, 'VERSION')).read().strip()

desc_lines = open('README', 'r').readlines()

setup(name='oldowan.%s' % PACKAGE,
      version=VERSION,
      description=desc_lines[0],
      long_description=''.join(desc_lines[2:]),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Scientific/Engineering :: Bio-Informatics"
      ],
      keywords='',
      platforms=['Any'],
      author='Ryan Raaum',
      author_email='code@raaum.org',
      url='http://www.raaum.org/software/oldowan',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=False,
      namespace_packages = ['oldowan'],
      install_requires=[
          "oldowan.polymorphism >= 1.0.0",
          "oldowan.mtconvert >= 1.0.0",
          "oldowan.fasta >= 1.0.0",
          "PyYAML",
          "networkx",
      ],
      zip_safe=False,
      data_files=[("oldowan/%s" % PACKAGE, ["oldowan/%s/VERSION" % PACKAGE]),
                  ("data/", ["data/hvr1_motifs.yaml", "data/motifs.shelved"])],
      entry_points = {
          'console_scripts': [
              'mitotype = oldowan.mitotype.commandline:run_command',
          ],
      },
      test_suite = 'nose.collector',
      )
