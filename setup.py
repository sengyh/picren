from setuptools import setup, find_packages

setup(
    name='picren',
    version='0.0.8',
    pymodules='picren',
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': ['picren= picren:picren',
                            ],
    },
)
