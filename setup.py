from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.lst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Oculi',
    version='0.1.0',
    description='Picamera control restful services',
    long_description=long_description,
    author='Jun Tan',
    author_email='jforce716@gmail.com',
    classifier=[
        'Development Status :: 3 - Alpha',
        'Topic :: PiCamera :: Web application :: Motion detect',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='PiCamera, restful interfaces, montion detect',
    packages=find_packages(where='./oculi'),
    install_requires=['flask', 'picamera', 'Pillow']
)
    
