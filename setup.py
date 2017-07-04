#!/usr/bin/env python3

# doc page:
# https://docs.python.org/3.5/distutils/setupscript.html
from setuptools import setup

setup(
	name = 'babybrowser',
	version = '0.1',
	description = 'Place holder...',
	author = 'Lauryn Brown',
	author_email = '',
	license = '',
	url = 'https://github.com/aanunez/babybrowser-fork',
	packages = ['babybrowser'],
	install_requires = [PyQt5],
	include_package_data = True,
    entry_points={
        'console_scripts': [
            'babybrowser = babybrowser.__main__:main'
        ]
    },
    classifiers=[
        # List here: https://pypi.python.org/pypi?%3Aaction=browse
        'Development Status :: 4 - Beta',
        #'Intended Audience :: Developers',
        #'Topic :: Software Development',
        #'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=''
)
