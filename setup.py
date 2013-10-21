#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# setup.py
#
# Copyright © 2013 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

setup(
    name='pytimeo',
    version='0.0.2',
    description='Interface between Python and SETRAM\'s service Timeo',
    author='Mathieu (matael) Gaborit',
    author_email='mathieu@matael.org',
    license='GNU/GPL',
    url='https://github.com/Matael/pytimeo',
    py_modules=['pytimeo'],
    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta'
    ],
)
