#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# setup.py
#
# Copyright © 2013 Mathieu Gaborit (matael) <mathieu@matael.org>
#
#
# Distributed under WTFPL terms
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#

from distutils.core import setup
from pytimeo import __version__

setup(
    name='pytimeo',
    version=__version__,
    description='Interface between Python and SETRAM\'s service Timeo',
    author='Mathieu (matael) Gaborit',
    author_email='mathieu@matael.org',
    url='http://blog.matael.org/',
    py_modules=['pytimeo']


)
