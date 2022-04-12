#  bdateutil
#  -----------
#  Adds business day logic and improved data type flexibility to
#  python-dateutil. 100% backwards compatible with python-dateutil,
#  simply replace dateutil imports with bdateutil.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Author:  Mark Guzman <segfault@hasno.info>
#  Website: https://github.com/segfault/bdateutil
#  License: MIT (see LICENSE file)


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='bdateutil',
    version='0.4.0',
    author='Tyler Copple',
    author_email='j.tylercopple@gmail.com',
    url='https://github.com/tcopple/bdateutil',
    license='MIT',
    packages=['bdateutil'],
    description=("Adds business day logic and improved data type flexibility "
                 "to python-dateutil."),
    long_description=open('README.rst').read(),
    install_requires=['python-dateutil', 'holidays'],
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: 3.9',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
    ],
)
