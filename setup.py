#!/usr/bin/env python
from distutils.core import setup


pname = "takeevery"
setup(name=pname, version="0.0.1",
      description="Generator helpers to take/iterate over every n elements "
                  "from a possibly infinite iterable.",
      author="Cong Ma",
      author_email="cong.ma@obspm.fr",
      url="https://gitlab.com/congma/takeevery/",
      py_modules=[pname],
      requires=["six"],
      provides=[pname])

