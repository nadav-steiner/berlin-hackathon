from setuptools import setup, find_packages

setup(
    name='analyzer1',
    packages=['analyzer'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        '''
        aiohttp
        numpy
        statsmodels
        click
        '''
    ],
    entry_points={
        'console_scripts': ['analyzer=analyzer_ts:entry']
    }
)
