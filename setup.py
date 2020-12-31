from setuptools import setup, find_packages
import os
setup(
    name="spiderlog",
    version="0.0.93",
    description="Static Site Generater",
    author="Lusaca",
    packages=find_packages(),
    install_requires=["libsass","Pillow","css-html-js-minify","Jinja2"],
    entry_points={
        "console_scripts": [
            "spiderlog=spiderlog.core:main",
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
)