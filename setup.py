from setuptools import setup, find_packages

setup(
    name='picren',
    version='1.0.0',
    author='sengyh',
    author_email='sengyh.dev@gmail.com',
    pymodules='picren',
    install_requires=[
        'Python3',
        'pathlib',
        'Click',
        'sqlalchemy',
        'alive_progress',
        'geopy',
    ],
    entry_points={
        'console_scripts': ['picren= picren:picren',
                            ],
    },
)
