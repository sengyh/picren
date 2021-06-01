from setuptools import setup, find_packages

setup(
    name='picren',
    version='1.0.0',
    author='sengyh',
    author_email='sengyh.dev@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    pymodules='picren',
    install_requires=[
        'pathlib',
        'Click',
        'sqlalchemy',
        'alive_progress',
        'geopy',
    ],
    entry_points={
        'console_scripts': ['picren= src.scripts.picren:picren',
                            ],
    },
)
