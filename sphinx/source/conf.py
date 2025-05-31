# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
os.environ['PYTHONPATH'] = os.path.abspath('../..')


# -- Project information -----------------------------------------------------

project = 'crsq'
copyright = '2023, Hideo Takahashi'
author = 'Hideo Takahashi'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.graphviz",
    "sphinxcontrib.mermaid",
    "sphinxcontrib.drawio",
#    "nbsphinx"
    "myst_nb",
    "sphinxcontrib.bibtex"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
# html_theme = 'furo'  # requires sphinx 6.0
html_theme = 'sphinx_book_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
numfig = True

# -- Options for autodoc -----------------------------------------------------
autodoc_typehints = 'description'
autoclass_content = 'both'

# -- Options for my-stnb -----------------------------------------------------
nb_execution_timeout = 60

# -- Options for bibtex ------------------------------------------------------
bibtex_bibfiles = ['refs.bib']
