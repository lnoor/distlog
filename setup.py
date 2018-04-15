
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='distlog',
    version='0.1dev',

    description='Logging for distributed systems.',
    long_description=long_description,
    url='https://github.com/lnoor/distlog',

    author='Leo Noordergraaf',
    author_email='leo@noordergraaf.net',

    license='GPLv3',
    platforms='any',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Logging',
        'Topic :: Utilities'
    ],

    keywords='scoped structured distributed logging',
    packages=find_packages(),
    package_data={
        '': ['LICENSE']
    },

    #install_requires=['docutils', 'requests', 'jsonpointer', 'pyyaml']
)
