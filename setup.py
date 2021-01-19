import io
import os
import re

"""
import logic_bank_utils.util as logic_bank_utils
(did_fix_path, sys_env_info) = \
    logic_bank_utils.add_python_path(project_dir="ApiLogicServer", my_file=__file__)
"""

from setuptools import find_packages, setup

find_version = True
if find_version:
    with io.open("app_logic_server/create_server.py", "rt", encoding="utf8") as f:
        version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)
else:
    version = 0.0


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname)).read()


def desc():
    return read("README.rst")


project_urls = {
  'Docs': 'https://github.com/valhuber/logicbank/wiki'
}

setup(
    name="apilogicserver",
    version=version,
    url="https://github.com/valhuber/ApiLogicServer",
    license="BSD",
    author="Val Huber",
    author_email="valjhuber@gmail.com",
    project_urls=project_urls,
    description=(
        "Create JSON:API and Web App from database, with LogicBank -- "
        "40X more concise, Python for extensibility."
    ),
    long_description=desc(),
    long_description_content_type="text/x-rst",
    # packages=find_packages(include=['logic_bank']),
    packages=['app_logic_server', 'expose_existing', 'expose_existing.sqlacodegen',
              'expose_existing.sqlacodegen.sqlacodegen'],
    package_data={"": ["LICENSE"]},
    entry_points={
        "console_scripts": ["create_server=app_logic_server.create_server:start"]
    },
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=[
        "Flask-Cors>=3.0.0",
        "inflect>=5.0.2",
        "safrs>=2.10.7",
        "logicbankutils>=0.6.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires="~=3.8"
)