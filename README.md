# SMQTK - Core

## Intent
Provide a light-weight framework for developing interfaces that have built-in
implementation discovery and factory construction from configuration.

## This looks a lot like KWIVER! Why use this instead?
[KWIVER](https://github.com/kitware/kwiver) is another open source package that
similarly holds modularity, plugins and configurability at its core.

The SMQTK-* suite of functionality exists separately from KWIVER for a few
reasons (for now):
* History
  * The origins of KWIVER and SMQTK were initiated at roughly the same
    time and were never resolved into the same thing because...
* Language
  * KWIVER has historically been predominantly C++ while SMQTK-* is (mostly)
    pure python. (see note below)
* Configuration UX
  * SMQTK takes an "add on" approach to configurability: concrete
    implementations have parameterized constructors and should be usable after
    construction like a "normal" object.
    Configuration semantics are derived from introspection of, and explicitly
    related to, the constructor.
    KWIVER takes an alternative approach where construction is generally empty
    and configuration setting is a required separate step via a custom object
    (`ConfigBlock`).
* Pythonic Plugin Support
  * Plugins are exposed via standard package entrypoints.

> If I'm using python, does that mean that SMQTK is __*always*__ the better
> choice?

At this point, not necessarily.
While this used to be true for a number of years due to SMQTK being the toolkit
with python support.
This is becoming more blurry KWIVER's continuously improving python binding
support.

## Building Documentation
https://smqtk-core.readthedocs.io/en/stable/

You can also build the sphinx documentation locally for the most up-to-date
reference:
```bash
# Install dependencies
poetry install
# Navigate to the documentation root.
cd docs
# Build the docs.
poetry run make html
# Open in your favorite browser!
firefox _build/html/index.html
```
