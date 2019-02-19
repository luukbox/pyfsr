from setuptools import setup
from pyfsr import name, version

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author='Lukas S. Müller',
    author_email='lukassebastianmueller@gmail.com',
    name=name,
    url='https://github.com/luukbox/pyfsr',
    version=version,
    description='a Feedback Shift Register library for python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['pyfsr'],
    keywords=['fsr', 'lfsr', 'nfsr', 'nlfsr'],
    install_requires=[
        'numpy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
    ],
    platforms=['any'],
)
