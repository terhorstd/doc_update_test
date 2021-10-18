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
import urllib3
import subprocess
# import sys
# sys.path.insert(0, os.path.abspath('.'))

#
# fetch patch for documentation
# Note: always fetch patch from latest repository (main)
#
http = urllib3.PoolManager()
patch = http.request("GET", "https://github.com/terhorstd/doc_update_test/raw/main/doc/patches/somediff.patch")
print(f"Fetched somediff.patch: {patch.status}")
if patch.status == 200:
    print(patch.data.decode('utf8'))
    print("<end of file>")

    # apply patch to current documentation
    with open("somediff.patch", "wb") as outfile:
        outfile.write(patch.data)
    print("patching...")
    patchresult = subprocess.run("patch -p2", shell=True, capture_output=True, input=patch.data)
    print(f"patch finished ({patchresult.returncode})")
    print(f"stdout:\n{patchresult.stdout.decode('utf8')}")
    print(f"stderr:\n{patchresult.stderr.decode('utf8')}")
    print("<end of patch>")
else:
    print("\nFAILED to download a patch! Assuming no patch for this version.\n")
    print(f"Received:\n{patch.data}\n<eot>")

# create job environment docs
with open("env.rst", "w", encoding="utf8") as outfile:
    outfile.write("RTD environment\n")
    outfile.write("---------------\n\n")
    outfile.write(".. :code-block:\n\n")
    for key, value in os.environ.items():
        outfile.write(f"    {key} = {value}\n")
    outfile.write("\n")

# show modified files in output
for name in ['env.rst', 'index.rst']:
    with open(name, 'r', encoding="utf8") as infile:
        print(f"--- {name} ---\n{infile.read()}--- eof {name} ---")

# -- Project information -----------------------------------------------------

project = 'DocUpdate Test'
copyright = '2021, terhorstd'
author = 'terhorstd'

# The full version, including alpha/beta/rc tags
release = '0.1rc1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
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
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
