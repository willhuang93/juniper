from setuptools import setup, find_packages

setup(
    name='juniper',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'pytest',
        'pyyaml',
    ],
    entry_points={
        "console_scripts": [
            "jnpr = src.jnpr:cmd",
        ]
    }
)
