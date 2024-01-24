from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join(this_directory, "requirements.txt")) as f:
    requirements = f.read().splitlines()

setup(
    name="ezsession",
    version="0.0.13",
    description="A small useful Python module to abstract away the common auth header methods used by different software vendors. The output is a requests session with the authentication headers built in.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Josh XT",
    author_email="josh@devxt.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=requirements,
)
