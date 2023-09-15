#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = []

test_requirements = [
    "pytest>=3",
]

setup(
    author="AI Maintainer Inc",
    author_email="douglas@ai-maintainer.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="A git util for working with the AI Maintainer go git repo in google cloud",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="ai_maintainer_git_util",
    name="aim_git_util",
    packages=find_packages(include=["aim_git_util", "aim_git_util.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/ai-maintainer-inc/ai_maintainer_git_util",
    version="0.1.2",
    zip_safe=False,
)
