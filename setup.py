#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='yaml_tags',
    version='0.0.1',
    url='https://github.com/anjianshi/yaml_tags',
    license='MIT',
    author='anjianshi',
    author_email='anjianshi@gmail.com',
    description="基于 pyyaml，提供一些辅助的 tag",
    packages=["yaml_tags"],
    install_requires=["pyyaml"],
    zip_safe=False,
    platforms='any',
    keywords=["yaml"],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
    ],
)
