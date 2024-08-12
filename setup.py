#!/usr/env python3

from setuptools import setup, find_packages
import gmbox_kvm_dbus

setup(
    name="gmbox-kvm-dbus",
    version=gmbox_kvm_dbus.__version__,
    packages=find_packages(),
    author="Getmobit",
    author_email="support@getmobit.ru",
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: POSIX :: Linux'
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
            'gmbox-kvm-dbus = gmbox_kvm_dbus.main:main',
        ]
    },
    python_requires='>=3.7',
    install_requires=[
        'dbus-next== 0.1.4.1'
    ],
    extras_require={
        'testing': [
            'pytest<6.2.0',
            'pytest-cov==2.12.1',
            'coverage==5.5',
            'flake8==3.9.2',
            'flake8-absolute-import==1.0.0.1',
            'flake8-import-order==0.18.1',
            'flake8-pep3101==1.3.0',
            'flake8-print==5.0.0',
            'pycodestyle==2.7.0'
        ]
    },
    include_package_data=True
)
