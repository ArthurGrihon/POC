Installation
============

These instructions will get you a copy of the project up and running on
your local machine for testing purposes only.

Prerequisites
-------------

The project runs with Python 3.8.10 and Python
libraries. Any desktop operating system supported by Python should work.

Installing the dependencies
---------------------------

A regular installation of Python and the project\'s dependencies would
work, but it is preferable to create a separate virtual environment with
the good version of the libraries. This can prevent this installation to
interfere with possible others.

First, create the virtual envionment for the project in Powershell:

    python -m venv .venv

Then, activate the environment:

    .\.venv\Scripts\activate.bat

Finally, install the dependencies inside the virtual environment:

    python -m pip install -r requirements.txt

Using it as a pip module
------------------------

### Installation

Activate the virtual environment:

    .\.venv\Scripts\activate.bat

You should see `(.venv)` at the beginning of the current shell line.
Then, upgrage pip:

    python -m pip install --upgrade pip

Upgrage the build module:

    python -m pip install --upgrade build

Build a local installable pip package:

    python -m build

Install this package so it can be imported any time in this virtual
environment:

    python -m pip install .

### Usage

--------------------

### Launch

The activating step should be executed each time you wish to run the
project:

    .\.venv\Scripts\activate.bat

You should see `(.venv)` at the beginning of the current shell line.

Navigate to the folder where the programs are and run a program. For
example:

### Deactivation

Note: If you want to deactivate the environment to go back to your
regular shell, just type:

    .\.venv\Scripts\deactivate.bat

Generating the doc
------------------

### Installation

The documentation needs to be generated to be accessed through a web
browser. First, install the dependencies:

    python -m pip install sphinx
    python -m pip install sphinx-rtd-theme
    python -m pip install sphinx-autodoc-typehints
    python -m pip install sphinxcontrib.plantuml

The diagrams need a PlantUML .jar file. Download it from [PlantUML
website](https://plantuml.com/download). Then open `docs/source/conf.py`
and modify the line
`plantuml = 'java -jar "C:/Users/fmonniot/Documents/Logiciels/plantuml.jar"'`
to fit the path to the PlantUML .jar file on your computer.

### Generation

You can generate the documentation using the following command:

    sphinx-build -b html docs/source/ docs/build/html

The generated HTML files are in `docs/build/html`
