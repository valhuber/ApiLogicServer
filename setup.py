import io
import os
import re

from setuptools import find_packages, setup

find_version = True
if find_version:
    with io.open("api_logic_server_cli/cli.py", "rt", encoding="utf8") as f:
        version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)
else:
    version = 0.0


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname)).read()


def desc():
    return read("README.md")


project_urls = {
  'Docs': 'https://github.com/valhuber/ApiLogicServer#readme'
}

setup(
    name="ApiLogicServer",
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
    long_description_content_type="text/markdown",
    packages=['api_logic_server_cli',
              'expose_existing', 'expose_existing.sqlacodegen', 'expose_existing.sqlacodegen.sqlacodegen',
              'prototype', 'prototype.api', 'prototype.database', 'prototype.logic', 'prototype.test',
              'prototype.templates', 'prototype.ui'],
    package_data={"api_logic_server_cli": ["nw.sqlite", "nw-gold.sqlite", "nw_logic.py", "nw_expose_services.py",
                                           "create_admin.sh", "nw_models_ext.py", "nw_server_startup_test.py",
                                           "ui_basic_web_app_run.py"],
                  "prototype": ["requirements.txt", "default.env", "EXAMPLE.env", "readme.md"],
                  'prototype.templates': ["index.html"]
                  },
    entry_points={
        "console_scripts": ["ApiLogicServer=api_logic_server_cli.cli:start"]
    },
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=[
        "PyJWT==1.7.1",
        "python-dateutil==2.8.1",
        "six==1.15.0",
        "SQLAlchemy==1.3.24",
        "SQLAlchemy-Utils==0.36.8",
        "Flask-AppBuilder==3.3.0",
        "logicbankutils==0.6.0",
        "inflect==5.0.2",
        "safrs>=2.11.4",
        "Flask-Admin==1.5.7",
        "Flask-Cors==3.0.0",
        "Flask==1.1.2",
        "Flask-Admin==1.5.7",
        "python-dotenv==0.15.0",
        "email-validator==1.1.1",
        "LogicBank>=1.0.0",
        "PyMySQL>=1.0.2",
        "cryptography>=3.3.1",
        "requests>=2.25.1"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires="~=3.8"
)