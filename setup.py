from setuptools import setup


setup(
    name='weewx-orm',
    packages=['weewx_orm'],
    version='1.0.0'
    include_package_data=True,
    install_requires=[
        'marshmallow-sqlalchemy',
        'msgpack-python',
        'sqlalchemy',
        'sqlalchemy-utils',
    ]
)
