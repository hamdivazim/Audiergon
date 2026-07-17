import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "Audiergon"
copyright = "2026, Hamd Waseem"
author = "Hamd Waseem"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

html_theme = "sphinx_rtd_theme"