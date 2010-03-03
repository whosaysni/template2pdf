import sys
from distutils.core import setup
try:
    from setuptools import setup
except ImportError:
    pass

version = '0.2'

setup(name="template2pdf",
      version=version,
      description="Generates PDF via trml2pdf using template engine(s).",
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
      author="Yasushi Masuda, Accense Technology, Inc.",
      author_email="ymasuda at accense.com or whosaysni at gmail.com",
      url="http://code.google.com/p/template2pdf/",
      license="LGPL",
      zip_safe=False,
      packages=["template2pdf", "template2pdf/django",
                "template2pdf/django/templatetags"],
      package_data={"template2pdf/django/templates/": "*",
                    "template2pdf/django/resources": "*",},
      )