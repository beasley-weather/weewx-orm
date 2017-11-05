from setuptools import setup


setup(
    name='weewx-orm',
    packages=['weewx_orm'],
    include_package_data=True,
    install_requires=['sqlalchemy']
)
