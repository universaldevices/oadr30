from setuptools import setup, find_packages

setup(
    name='oadr30',
    version='1.0.0',
    packages=find_packages(),
    description='OpenADR 3.0 Reference VEN Implementation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Michel Kohanim',
    author_email='support@universal-devices.com',
    url='https://github.com/universaldevices/oadr30.git',
    install_requires=[
	'jsonschema>=4.17.3',
	'pytz>=2023.3',
	'requests>=2.25.1',
	'schedule>=1.2.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
