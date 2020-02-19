# -*- coding: utf-8 -*-
import os
import re
import codecs

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


long_desc = '''
Blanket is an extension to reStructuredText and Sphinx to be able to read and
 render coverage xml output.
'''

requires = ['Sphinx>=2.0', 'docutils>=0.12']

setup(
    name='blanket',
    version=find_version("src", "blanket", "__init__.py"),
    url='https://github.com/hsorby/blanket',
    download_url='https://github.com/hsorby/blanket',
    license='Apache 2.0',
    author='Hugh Sorby',
    author_email='h.sorby@auckland.ac.nz',
    description='Sphinx Coverage renderer',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache 2.0 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    platforms='any',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    # entry_points={
    #     'console_scripts': [
    #         'breathe-apidoc = breathe.apidoc:main',
    #     ],
    # },
    install_requires=requires,
)
