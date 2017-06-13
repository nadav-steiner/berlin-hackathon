from setuptools import setup, find_packages

setup(
    name='analyzer1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        '''
        aiohttp
        numpy
        statsmodels
        '''
    ],
    entry_points={
        'console_scripts': ['analyzer=analyzer_ts:entry']
    }
)
