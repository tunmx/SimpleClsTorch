#!/usr/bin/env python
from setuptools import find_packages, setup

__version__ = "0.0.1"

if __name__ == "__main__":
    setup(
        name="simplecls",
        version=__version__,
        description="Deep Learning Simple Classification",
        url="https://github.com/tunmx/SimpleClsTorch",
        author="Tunm",
        author_email="tunmxy@163.com",
        keywords="Deep Learning",
        # packages=find_packages(exclude=("config", "demo")),
        classifiers=[
            "Development Status :: Beta",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
        ],
        license="Apache License 2.0",
        zip_safe=False,
        entry_points="""
            [console_scripts]
            bvt=simplecls.command.cli:cli
        """
    )
