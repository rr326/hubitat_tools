from distutils.core import setup

setup(
    name='HTools',
    version='0.0.1',
    packages=['python_app',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    install_requires=[
        'flask',
        'flask_cors',
        'click',
        'requests'
    ]
)
