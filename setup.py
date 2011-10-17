from setuptools import setup, find_packages

setup(name="pyumpf", 
    version="0.1.1", 
    author="Adam Faulconbridge", 
    author_email="afaulconbridge@googlemail.com", 
    packages = find_packages(),
    classifiers = ["Development Status :: 3 - Alpha", 
        "Intended Audience :: Developers", 
        "License :: OSI Approved :: BSD License", 
        "Natural Language :: English", 
        "Operating System :: OS Independent", 
        "Programming Language :: Python", 
        "Programming Language :: Python :: 2.6", 
        "Programming Language :: Python :: 2.7", 
        "Topic :: Software Development :: Libraries :: Python Modules"], 
    url="https://github.com/afaulconbridge/pyumpf", 
    description="Python Unified Multiprocessing Parallel Functions", 
    long_description=open("README.txt").read() )
