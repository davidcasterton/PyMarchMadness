import codecs
import os
import pdb

from setuptools import setup, find_packages


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "PyMarchMadness"
DESCRIPTION = "Python March Madness analysis"
AUTHOR = __import__(NAME).__author__
AUTHOR_EMAIL = __import__(NAME).__email__
VERSION = __import__(NAME).__version__
LICENSE = __import__(NAME).__license__
URL = ""

package_data = []
INPUT_DATA = os.path.join('PyMarchMadness', 'InputData')
for file in os.listdir(INPUT_DATA):
    package_data.append(os.path.join('InputData', file, "*"))

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=URL,
    packages=find_packages(),
    package_data={NAME: package_data},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    zip_safe=False,
)