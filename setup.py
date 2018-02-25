from setuptools import setup


setup(
    name='weewx-orm',
    author='francium',
    description='A library for interfacing with the Weewx database layer.'
    url='https://github.com/beasley-weather/weewx-orm'
    license='MIT',
    version='1.0.0',
    packages=['weewx_orm'],
    include_package_data=True,
    install_requires=[
        'marshmallow-sqlalchemy',
        'sqlalchemy',
        'sqlalchemy-utils',
    ]
)
