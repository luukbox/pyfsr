from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as fh:
    install_requires = fh.read().splitlines()

setup(
    author='Lukas Sebastian Müller',
    author_email='lukassebastianmueller@gmail.com',
    name='pyfsr',
    url='https://github.com/luukbox/pyfsr',
    version='1.0',
    description='a Feedback Shift Register toolkit for python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['pyfsr'],
    keywords=['fsr', 'lfsr', 'nfsr', 'nlfsr'],
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
    ],
    platforms=['any'],
)
