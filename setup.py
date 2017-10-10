from distutils.core import setup
from setuptools import find_packages

setup(
    name='heresy',
    python_requires='>=3',
    version='0.11',
    author='Andreas Dewes - 7scientists',
    author_email='andreas@7scientists.com',
    license='MIT',
    url='https://github.com/adewes/heresy',
    packages=find_packages(),
    package_data={'': ['*.ini']},
    include_package_data=True,
    install_requires=['six', 'click'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'heresy = heresy.cli.main:heresy'
        ]
    },
    description='A simple yet powerful templating system for Python.',
    long_description="""A simple yet powerful templating system for Python. 
"""
)
