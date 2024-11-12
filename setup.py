from setuptools import setup, find_packages

setup(
    name='cookie_database',
    version='0.1',
    packages=['Database', 'Database.models'],
    install_requires=[
        'sqlalchemy',
        'pymysql',
    ],
)
