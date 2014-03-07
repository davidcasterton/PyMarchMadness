import codecs
import os
import pdb

from setuptools import setup, find_packages


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "PyMarchMadness"
DESCRIPTION = "Python March Madness analysis."
AUTHOR = "David Casterton"
AUTHOR_EMAIL = ""
URL = ""
VERSION = __import__(NAME).__version__
INPUT_DATA = os.path.join('PyMarchMadness', 'InputData')

package_data = []
for file in os.listdir(INPUT_DATA):
    package_data.append(os.path.join(file, "*"))

pdb.set_trace()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="GPLv3",
    url=URL,
    packages=['PyMarchMadness'],
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