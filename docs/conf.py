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
sys.path.insert(0, os.path.abspath('../'))


# -- Project information -----------------------------------------------------

project = 'Luster'
copyright = '2022, I. Ahmad (izxxr)'
author = 'I. Ahmad (izxxr)'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "aiohttp": ("https://docs.aiohttp.org/en/stable", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
html_logo = "assets/logo.png"

# These color options have been copied from Revolt theme.
html_theme_options = {
    "light_css_variables": {
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f6f6f6",
        "color-sidebar-background": "#f1f1f1",
        "color-brand-primary": "#ff4655",
        "color-brand-content": "#ff4655",
    },
    "dark_css_variables": {
        "color-background-primary": "#242424",
        "color-background-secondary": "#181818",
        "color-sidebar-background": "#1e1e1e",
        "color-brand-primary": "#ff4655",
        "color-brand-content": "#ff4655",
    }
}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

_attachment_parameter_note = (
    "If a :class:`str` is passed, It is considered the attachment ID and is passed directly. "
    "If a :class:`io.BufferedReader` is passed, It will be automatically uploaded to file server "
    "first using :meth:`HTTPHandler.upload_file`"
)

rst_prolog = f"""
.. |attachment-parameter-note| replace:: {_attachment_parameter_note}
"""


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
