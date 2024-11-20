from setuptools import setup, find_packages

setup(
    name='oadr30_ven_ud',
    version='1.0.3',
    packages=find_packages(),
    description='Open Source OpenADR 3.0 VEN Implementation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Michel Kohanim',
    author_email='support@universal-devices.com',
    url='https://github.com/universaldevices/oadr30.git',
    install_requires=[
	'requests>=2.25.1',
    'isodate>=0.6.1',
    'pytz>=2024.1',
    'tzlocal>=4.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
